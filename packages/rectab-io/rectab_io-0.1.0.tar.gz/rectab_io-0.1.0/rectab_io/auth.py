import uuid
from .config import load_config, save_config
from .email_service import send_access_token_email

def generate_access_token() -> str:
    """Generate a secure unique access token"""
    return str(uuid.uuid4())

def setup_user():
    """Prompt user for details, generate token, send email and save config"""
    print("🔧 Welcome to Rectab.io Initial Setup")
    print("Please fill the following details to get your access token\n")
    
    user_email = input("Enter Your Email: ").strip()
    user_fullname = input("Enter Your Full Name: ").strip()

    # Validate inputs
    if not user_email or "@" not in user_email:
        raise ValueError("Please enter a valid email address")
    if not user_fullname:
        raise ValueError("Full name cannot be empty")

    # Generate token
    access_token = generate_access_token()

    # Send email
    print(f"\n📧 Sending access token to {user_email}...")
    email_sent = send_access_token_email(user_email, user_fullname, access_token)
    
    if not email_sent:
        print("⚠️  Email could not be sent, but your token has been saved locally.")
        print(f"Your access token is: {access_token}")

    # Save config
    config = {
        "user_email": user_email,
        "full_name": user_fullname,
        "access_token": access_token,
        "is_authenticated": True
    }
    save_config(config)
    print("\n✅ Setup completed successfully! You can now use Rectab.io analytics.")

def validate_auth() -> bool:
    """Validate if user is authenticated with valid token"""
    config = load_config()
    if not config or not config.get("is_authenticated") or not config.get("access_token"):
        print("❌ You are not authenticated. Please complete the setup first.")
        setup_user()
        return True
    return True