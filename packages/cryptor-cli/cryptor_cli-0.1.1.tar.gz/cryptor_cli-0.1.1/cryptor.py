# cryptor.py
import os
import click
import sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.keywrap import aes_key_wrap, aes_key_unwrap
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag, InvalidKey
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# --- Constants ---
MKEK_SALT_SIZE = 16  # Salt for the Master Key Encryption Key
ARGON2_ITERATIONS = 3
ARGON2_MEMORY_COST = 65536  # 64MB
ARGON2_LANES = 4

# AES-256-KW requires a 32-byte key
MKEK_SIZE = 32  # Master Key Encryption Key size
MASTER_KEY_SIZE = 32  # The main key used for wrapping data keys

# AES-256-GCM parameters for file encryption
DEK_SIZE = 32  # Data Encryption Key size
GCM_NONCE_SIZE = 12
GCM_TAG_SIZE = 16

# RSA parameters for remote key
RSA_KEY_SIZE = 4096 # Bits
RSA_PUBLIC_EXPONENT = 65537

# Filename for the master key file
MASTER_KEY_FILE = 'master.key'

# --- Master Key File Structure ---
# The master.key file will store a header, the password-wrapped master key,
# and optionally, an RSA public key and the master key wrapped by that RSA public key.
#
# Format:
#   MAGIC_BYTES (8 bytes) - "CRPT_V01"
#   MKEK_SALT (16 bytes)
#   WRAPPED_MASTER_KEY_BY_PASSWORD (40 bytes, since MASTER_KEY_SIZE 32 + 8 for AES-KW)
#   HAS_REMOTE_KEY (1 byte: 0x00 or 0x01)
#   If HAS_REMOTE_KEY is 0x01:
#       RSA_PUBLIC_KEY_LEN (4 bytes, big-endian)
#       RSA_PUBLIC_KEY_PEM (variable length)
#       WRAPPED_MASTER_KEY_BY_RSA (RSA_KEY_SIZE / 8 bytes)
#
MAGIC_BYTES = b"CRPT_V01"
MAGIC_BYTES_LEN = len(MAGIC_BYTES)
WRAPPED_MASTER_KEY_PASSWORD_LEN = MASTER_KEY_SIZE + 8 # AES-KW adds 8 bytes
HAS_REMOTE_KEY_FLAG_LEN = 1
RSA_PUBLIC_KEY_LEN_BYTES = 4 # For storing length of PEM
WRAPPED_MASTER_KEY_RSA_LEN = RSA_KEY_SIZE // 8 # RSA wraps to its key size

# --- Helper Functions ---

def derive_key_from_password(password: bytes, salt: bytes) -> bytes:
    """Derives a key from a password and salt using Argon2id."""
    kdf = Argon2id(
        salt=salt,
        length=MKEK_SIZE,
        iterations=ARGON2_ITERATIONS,
        lanes=ARGON2_LANES,
        memory_cost=ARGON2_MEMORY_COST
    )
    key = kdf.derive(password)
    return key

def _read_master_key_file_parts():
    """Reads raw parts from the master.key file."""
    try:
        with open(MASTER_KEY_FILE, 'rb') as f:
            magic = f.read(MAGIC_BYTES_LEN)
            if magic != MAGIC_BYTES:
                raise click.ClickException("Invalid master.key file format or version.")
            
            salt = f.read(MKEK_SALT_SIZE)
            wrapped_master_key_password = f.read(WRAPPED_MASTER_KEY_PASSWORD_LEN)
            
            has_remote_key_flag = f.read(HAS_REMOTE_KEY_FLAG_LEN)
            has_remote_key = (has_remote_key_flag == b'\x01')
            
            rsa_public_key_pem = None
            wrapped_master_key_rsa = None

            if has_remote_key:
                rsa_public_key_len_bytes = f.read(RSA_PUBLIC_KEY_LEN_BYTES)
                if not rsa_public_key_len_bytes:
                     raise click.ClickException("Corrupted master.key file: missing remote key length.")
                rsa_public_key_len = int.from_bytes(rsa_public_key_len_bytes, 'big')
                rsa_public_key_pem = f.read(rsa_public_key_len)
                wrapped_master_key_rsa = f.read(WRAPPED_MASTER_KEY_RSA_LEN)
                if not rsa_public_key_pem or not wrapped_master_key_rsa:
                     raise click.ClickException("Corrupted master.key file: missing remote key data.")

            return magic, salt, wrapped_master_key_password, has_remote_key, rsa_public_key_pem, wrapped_master_key_rsa
    except FileNotFoundError:
        raise click.ClickException(f"Master key file '{MASTER_KEY_FILE}' not found. Please generate it first.")
    except Exception as e:
        raise click.ClickException(f"An error occurred while reading the master key file: {e}")

def _write_master_key_file(salt, wrapped_master_key_password, has_remote_key, rsa_public_key_pem, wrapped_master_key_rsa):
    """Writes all parts to the master.key file."""
    try:
        with open(MASTER_KEY_FILE, 'wb') as f:
            f.write(MAGIC_BYTES)
            f.write(salt)
            f.write(wrapped_master_key_password)
            
            if has_remote_key and rsa_public_key_pem and wrapped_master_key_rsa:
                f.write(b'\x01') # Has remote key
                rsa_public_key_len = len(rsa_public_key_pem)
                f.write(rsa_public_key_len.to_bytes(RSA_PUBLIC_KEY_LEN_BYTES, 'big'))
                f.write(rsa_public_key_pem)
                f.write(wrapped_master_key_rsa)
            else:
                f.write(b'\x00') # Does not have remote key
    except Exception as e:
        raise click.ClickException(f"An error occurred while writing to the master key file: {e}")

def load_master_key_with_password(password: str) -> bytes:
    """Loads, decrypts, and returns the master key from the master.key file using password."""
    magic, salt, wrapped_master_key_password, _, _, _ = _read_master_key_file_parts()

    try:
        mKEK = derive_key_from_password(password.encode(), salt)
        master_key = aes_key_unwrap(mKEK, wrapped_master_key_password)
        return master_key
    except InvalidKey:
        raise click.ClickException("Invalid password or corrupted master key file.")
    except Exception as e:
        raise click.ClickException(f"An error occurred while loading the master key with password: {e}")

def load_master_key_with_remote_key(private_key_path: str) -> bytes:
    """Loads, decrypts, and returns the master key using a remote private key."""
    magic, salt, wrapped_master_key_password, has_remote_key, rsa_public_key_pem, wrapped_master_key_rsa = _read_master_key_file_parts()

    if not has_remote_key:
        raise click.ClickException("Master key file does not contain a remote unlock key.")
    
    try:
        with open(private_key_path, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None, # Private key should ideally be protected by a passphrase
                backend=default_backend()
            )
        
        # Use the private key to decrypt the RSA-wrapped master key
        master_key = private_key.decrypt(
            wrapped_master_key_rsa,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return master_key
    except FileNotFoundError:
        raise click.ClickException(f"Private key file '{private_key_path}' not found.")
    except ValueError as e: # For bad private key format or passphrase
        raise click.ClickException(f"Invalid private key file or format: {e}")
    except Exception as e:
        raise click.ClickException(f"An error occurred while loading the master key with remote key: {e}")

# --- Click CLI Group Setup ---

@click.group()
def cli():
    """A CLI tool for secure file encryption using AES-256-GCM and Argon2."""
    pass

# --- Key Management Commands ---

@cli.group('manage-keys')
def manage_keys():
    """Commands for managing the master key."""
    pass

@manage_keys.command('generate')
def generate_master_key():
    """Generates a new master key and encrypts it with your password."""
    if os.path.exists(MASTER_KEY_FILE):
        click.confirm(f"⚠️  '{MASTER_KEY_FILE}' already exists. Overwrite it?", abort=True)

    password = click.prompt("Enter a new password for the master key", hide_input=True, confirmation_prompt=True)
    
    # 1. Generate the actual master key (this is what we protect)
    master_key = os.urandom(MASTER_KEY_SIZE)
    
    # 2. Generate a salt to derive the key that will encrypt the master key
    salt = os.urandom(MKEK_SALT_SIZE)
    
    # 3. Derive the Master Key Encryption Key (MKEK) from the password
    mKEK = derive_key_from_password(password.encode(), salt)
    
    # 4. Wrap (encrypt) the master key with the MKEK
    wrapped_master_key_password = aes_key_wrap(mKEK, master_key)
    
    # 5. Save the salt and the wrapped master key to a file (initially without remote key)
    _write_master_key_file(salt, wrapped_master_key_password, False, None, None)
        
    click.secho(f"✅ Master key generated and saved to '{MASTER_KEY_FILE}'.", fg='green')

@manage_keys.command('add-remote-key')
@click.argument('private_key_output_path', type=click.Path(dir_okay=False))
def add_remote_key(private_key_output_path):
    """
    Generates an RSA key pair, adds the public key to master.key,
    and stores the private key offline for remote master key unlocking/reset.
    """
    if not os.path.exists(MASTER_KEY_FILE):
        raise click.ClickException(f"Master key file '{MASTER_KEY_FILE}' not found. Generate it first.")

    magic, salt, wrapped_master_key_password, current_has_remote_key, _, _ = _read_master_key_file_parts()

    if current_has_remote_key:
        click.confirm(f"⚠️  '{MASTER_KEY_FILE}' already contains a remote key. Overwrite it?", abort=True)

    click.echo("Generating a new RSA key pair...")
    private_key = rsa.generate_private_key(
        public_exponent=RSA_PUBLIC_EXPONENT,
        key_size=RSA_KEY_SIZE,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Serialize private key to PEM (PKCS#8) - recommend passphrase protection for real use
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption() # For simplicity in CLI, but NOT recommended for production
    )

    # Save private key to user specified file
    try:
        with open(private_key_output_path, 'wb') as f:
            f.write(private_pem)
        os.chmod(private_key_output_path, 0o600) # Ensure private key is readable only by owner
        click.secho(f"✅ Private key saved to '{private_key_output_path}' with restricted permissions.", fg='green')
        click.secho("⚠️  KEEP THIS PRIVATE KEY FILE EXTREMELY SECURE AND OFFLINE!", fg='red')
    except Exception as e:
        raise click.ClickException(f"Failed to save private key: {e}")

    # Serialize public key to PEM
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Load master key with password (required to re-wrap with new RSA public key)
    password = click.prompt("Enter your current master key password", hide_input=True)
    master_key = load_master_key_with_password(password)

    # Wrap master key with RSA public key
    wrapped_master_key_rsa = public_key.encrypt(
        master_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    _write_master_key_file(salt, wrapped_master_key_password, True, public_pem, wrapped_master_key_rsa)
    click.secho(f"✅ Remote key added to '{MASTER_KEY_FILE}'.", fg='green')


@manage_keys.command('backup-master-key')
@click.argument('output_path', type=click.Path(dir_okay=False), default='cryptor_master.key.enc')
def backup_master_key(output_path):
    """
    Encrypts the master.key file using the embedded remote public key
    and saves it to a backup file. This backup can only be decrypted
    with the corresponding remote private key (stored offline).
    """
    if not os.path.exists(MASTER_KEY_FILE):
        raise click.ClickException(f"Master key file '{MASTER_KEY_FILE}' not found. Generate it first.")

    # Read the full content of the master.key file
    try:
        with open(MASTER_KEY_FILE, 'rb') as f:
            master_key_full_content = f.read()
    except Exception as e:
        raise click.ClickException(f"Failed to read '{MASTER_KEY_FILE}': {e}")

    # Extract the public key from the master.key structure
    magic, salt, wrapped_master_key_password, has_remote_key, rsa_public_key_pem, wrapped_master_key_rsa_from_file = _read_master_key_file_parts()

    if not has_remote_key:
        raise click.ClickException(f"'{MASTER_KEY_FILE}' does not contain an embedded remote public key. "
                                   f"Please use 'cryptor manage-keys add-remote-key <private_key_path>' first.")

    try:
        public_key = serialization.load_pem_public_key(
            rsa_public_key_pem,
            backend=default_backend()
        )

        # Encrypt the ENTIRE master_key_full_content with the remote public key
        encrypted_backup = public_key.encrypt(
            master_key_full_content,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        with open(output_path, 'wb') as f:
            f.write(encrypted_backup)

        click.secho(f"✅ Encrypted master key backup saved to '{output_path}'.", fg='green')
        click.secho("\n--- SECURE OFFLINE STORAGE INSTRUCTIONS ---", fg='cyan')
        click.secho(f"This file ('{output_path}') is encrypted with your remote PUBLIC key.", fg='cyan')
        click.secho("To decrypt it (e.g., if you lose your original master.key or forget its password), you will need the corresponding remote PRIVATE key file.", fg='cyan')
        click.secho(f"1. Store '{output_path}' in a safe, physically separate location (e.g., encrypted cloud storage, another drive, print as QR code).", fg='cyan')
        click.secho(f"2. Ensure your remote PRIVATE KEY (e.g., from 'cryptor manage-keys add-remote-key') is kept in an EXTREMELY SECURE AND OFFLINE location.", fg='red')
        click.secho("   - This usually means a USB drive stored in a safe, or a printed QR code of the private key.", fg='red')
        click.secho("   - NEVER store the PRIVATE KEY on the same system as the backup file.", fg='red')
        click.secho("Without both the backup file and the private key, recovery is impossible.", fg='red')

    except Exception as e:
        raise click.ClickException(f"Failed to create master key backup: {e}")


@manage_keys.command('change-password')
def change_master_key_password():
    """Changes the password for an existing master key."""
    if not os.path.exists(MASTER_KEY_FILE):
        raise click.ClickException(f"Master key file '{MASTER_KEY_FILE}' not found. Cannot change password.")

    old_password = click.prompt("Enter your current password", hide_input=True)
    
    # Read existing file parts
    magic, old_salt, old_wrapped_master_key_password, has_remote_key, rsa_public_key_pem, wrapped_master_key_rsa = _read_master_key_file_parts()

    try:
        # Load the master key using the old password
        master_key = load_master_key_with_password(old_password)
        
        # Get the new password
        new_password = click.prompt("Enter your new password", hide_input=True, confirmation_prompt=True)
        
        # Generate a new salt and derive a new MKEK
        new_salt = os.urandom(MKEK_SALT_SIZE)
        new_mKEK = derive_key_from_password(new_password.encode(), new_salt)
        
        # Re-wrap the master key with the new MKEK
        new_wrapped_master_key_password = aes_key_wrap(new_mKEK, master_key)
        
        # Write the updated master key file (keeping remote key info if present)
        _write_master_key_file(new_salt, new_wrapped_master_key_password, has_remote_key, rsa_public_key_pem, wrapped_master_key_rsa)
            
        click.secho("✅ Master key password changed successfully.", fg='green')
        
    except click.ClickException as e:
        click.secho(f"❌ Error: {e}", fg='red', err=True)

@manage_keys.command('reset-password-remote')
@click.argument('private_key_path', type=click.Path(exists=True, dir_okay=False))
def reset_password_remote(private_key_path):
    """Resets the master key password using an offline remote private key."""
    if not os.path.exists(MASTER_KEY_FILE):
        raise click.ClickException(f"Master key file '{MASTER_KEY_FILE}' not found. Cannot reset password.")

    click.echo(f"Attempting to reset password using private key from '{private_key_path}'...")
    
    # Read existing file parts
    magic, old_salt, old_wrapped_master_key_password, has_remote_key, rsa_public_key_pem, wrapped_master_key_rsa = _read_master_key_file_parts()
    
    try:
        # Load the master key using the remote private key
        master_key = load_master_key_with_remote_key(private_key_path)

        # Get the new password
        new_password = click.prompt("Enter your new password", hide_input=True, confirmation_prompt=True)

        # Generate a new salt and derive a new MKEK
        new_salt = os.urandom(MKEK_SALT_SIZE)
        new_mKEK = derive_key_from_password(new_password.encode(), new_salt)
        
        # Re-wrap the master key with the new MKEK
        new_wrapped_master_key_password = aes_key_wrap(new_mKEK, master_key)
        
        # Write the updated master key file (keeping remote key info if present)
        _write_master_key_file(new_salt, new_wrapped_master_key_password, has_remote_key, rsa_public_key_pem, wrapped_master_key_rsa)

        click.secho("✅ Master key password reset successfully using remote key.", fg='green')

    except click.ClickException as e:
        click.secho(f"❌ Error: {e}", fg='red', err=True)
    except Exception as e:
        click.secho(f"❌ An unexpected error occurred during remote password reset: {e}", fg='red', err=True)


@cli.command('encrypt')
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.argument('output_file', type=click.Path(dir_okay=False))
def encrypt(input_file, output_file):
    """Encrypts a file using envelope encryption."""
    password = click.prompt("Enter your master key password", hide_input=True)
    
    try:
        master_key = load_master_key_with_password(password)
        dek = os.urandom(DEK_SIZE)
        wrapped_dek = aes_key_wrap(master_key, dek)
        
        with open(input_file, 'rb') as f:
            plaintext = f.read()
        
        aesgcm = AESGCM(dek)
        gcm_nonce = os.urandom(GCM_NONCE_SIZE)
        ciphertext = aesgcm.encrypt(gcm_nonce, plaintext, None)
        gcm_tag = ciphertext[-GCM_TAG_SIZE:]
        encrypted_data = ciphertext[:-GCM_TAG_SIZE]
        
        with open(output_file, 'wb') as f:
            f.write(gcm_nonce)
            f.write(wrapped_dek)
            f.write(gcm_tag)
            f.write(encrypted_data)
            
        click.secho(f"✅ File '{input_file}' encrypted successfully to '{output_file}'.", fg='green')
        
    except click.ClickException as e:
        click.secho(f"❌ Error: {e}", fg='red', err=True)
    except Exception as e:
        click.secho(f"❌ An unexpected error occurred during encryption: {e}", fg='red', err=True)

@cli.command('decrypt')
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.argument('output_file', type=click.Path(dir_okay=False))
def decrypt(input_file, output_file):
    """Decrypts a file."""
    password = click.prompt("Enter your master key password", hide_input=True)
    
    try:
        master_key = load_master_key_with_password(password)
        
        with open(input_file, 'rb') as f:
            gcm_nonce = f.read(GCM_NONCE_SIZE)
            wrapped_dek_size = DEK_SIZE + 8
            wrapped_dek = f.read(wrapped_dek_size)
            gcm_tag = f.read(GCM_TAG_SIZE)
            ciphertext = f.read()
            
        dek = aes_key_unwrap(master_key, wrapped_dek)
        
        aesgcm = AESGCM(dek)
        ciphertext_with_tag = ciphertext + gcm_tag
        plaintext = aesgcm.decrypt(gcm_nonce, ciphertext_with_tag, None)
        
        with open(output_file, 'wb') as f:
            f.write(plaintext)
            
        click.secho(f"✅ File '{input_file}' decrypted successfully to '{output_file}'.", fg='green')
        
    except (click.ClickException, InvalidTag, InvalidKey) as e:
        click.secho(f"❌ Decryption failed. Check your password or file integrity. Error: {e}", fg='red', err=True)
    except Exception as e:
        click.secho(f"❌ An unexpected error occurred during decryption: {e}", fg='red', err=True)

if __name__ == '__main__':
    cli()