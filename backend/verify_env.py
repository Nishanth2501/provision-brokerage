#!/usr/bin/env python3
"""
Environment Variable Verification Script
Run this before deploying to ensure all required variables are set
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_env_var(name, required=True, description=""):
    """Check if an environment variable is set"""
    value = os.getenv(name)
    status = "✓" if value else "✗"
    req_text = "[REQUIRED]" if required else "[OPTIONAL]"
    
    if value:
        # Mask sensitive values
        if "KEY" in name or "SECRET" in name or "PASSWORD" in name:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"{status} {req_text} {name}: {masked}")
        else:
            print(f"{status} {req_text} {name}: {value}")
        return True
    else:
        print(f"{status} {req_text} {name}: NOT SET - {description}")
        return not required


def main():
    """Main verification function"""
    print("\n" + "="*70)
    print("🔍 PROVISION BROKERAGE - ENVIRONMENT VERIFICATION")
    print("="*70 + "\n")
    
    all_ok = True
    
    # Required variables
    print("📋 Required Variables:")
    print("-" * 70)
    all_ok &= check_env_var(
        "GROQ_API_KEY", 
        required=True, 
        description="Get from https://console.groq.com/keys"
    )
    all_ok &= check_env_var(
        "CALCOM_API_KEY", 
        required=True, 
        description="Get from https://app.cal.com/settings/developer"
    )
    all_ok &= check_env_var(
        "CALCOM_EVENT_TYPE_ID", 
        required=True, 
        description="Your Cal.com event type ID"
    )
    all_ok &= check_env_var(
        "CALCOM_USERNAME", 
        required=True, 
        description="Your Cal.com username"
    )
    
    print("\n📝 Optional Variables:")
    print("-" * 70)
    check_env_var("GROQ_MODEL", required=False, description="AI model name")
    check_env_var("CALCOM_API_URL", required=False, description="Cal.com API URL")
    check_env_var("DATABASE_URL", required=False, description="PostgreSQL connection string")
    check_env_var("DEBUG", required=False, description="Debug mode (true/false)")
    check_env_var("CORS_ORIGINS", required=False, description="Allowed CORS origins")
    
    print("\n🔧 SMS/WhatsApp Configuration (Optional):")
    print("-" * 70)
    check_env_var("SINCH_PROJECT_ID", required=False)
    check_env_var("SINCH_SERVICE_PLAN_ID", required=False)
    check_env_var("SINCH_ACCESS_KEY_ID", required=False)
    check_env_var("SINCH_KEY_SECRET", required=False)
    check_env_var("SINCH_PHONE_NUMBER", required=False)
    
    # Summary
    print("\n" + "="*70)
    if all_ok:
        print("✅ SUCCESS! All required environment variables are set.")
        print("="*70 + "\n")
        print("You're ready to deploy! 🚀")
        print("\nNext steps:")
        print("1. Push your code to GitHub")
        print("2. Go to https://dashboard.render.com")
        print("3. Create a new Blueprint")
        print("4. Select your repository")
        print("5. Enter these environment variables in Render")
        print("\nSee RENDER_QUICKSTART.md for detailed instructions.")
        return 0
    else:
        print("❌ MISSING REQUIRED VARIABLES")
        print("="*70 + "\n")
        print("Please set the required environment variables before deploying.")
        print("\nHow to set them:")
        print("1. Create a .env file in the backend directory")
        print("2. Add the missing variables (see .env.example)")
        print("3. For Render deployment, add them in the dashboard")
        print("\nSee DEPLOYMENT.md for more information.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

