#!/bin/bash

# ProVision Brokerage - Pre-Deployment Script
# This script helps you prepare for deployment to Render

echo "════════════════════════════════════════════════════════════════"
echo "   🚀 PROVISION BROKERAGE - RENDER DEPLOYMENT HELPER"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Step 1: Check if we're in the right directory
print_status "Checking project directory..."
if [ ! -f "render.yaml" ]; then
    print_error "render.yaml not found. Please run this script from the project root."
    exit 1
fi
print_success "Project directory confirmed"

# Step 2: Check if git is initialized
print_status "Checking git status..."
if [ ! -d ".git" ]; then
    print_warning "Git not initialized. Initializing now..."
    git init
    print_success "Git initialized"
else
    print_success "Git repository found"
fi

# Step 3: Verify Python environment
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
print_success "Found $PYTHON_VERSION"

# Step 4: Check for required files
print_status "Verifying required files..."
required_files=(
    "backend/main.py"
    "backend/requirements.txt"
    "backend/Procfile"
    "frontend/index.html"
    "frontend/config.js"
    "render.yaml"
)

all_files_present=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "$file"
    else
        print_error "$file NOT FOUND"
        all_files_present=false
    fi
done

if [ "$all_files_present" = false ]; then
    print_error "Some required files are missing. Please check your project structure."
    exit 1
fi

# Step 5: Verify environment variables
print_status "Checking environment variables..."
echo ""
echo "Running environment verification script..."
if [ -f "backend/verify_env.py" ]; then
    python3 backend/verify_env.py
    if [ $? -ne 0 ]; then
        echo ""
        print_warning "Some environment variables are not set."
        print_warning "This is OK for deployment - you'll set them in Render."
        echo ""
    fi
else
    print_warning "verify_env.py not found, skipping environment check"
fi

# Step 6: Check git status
echo ""
print_status "Checking for uncommitted changes..."
if git diff --quiet && git diff --staged --quiet; then
    print_success "No uncommitted changes"
else
    print_warning "You have uncommitted changes"
    echo ""
    git status --short
    echo ""
    read -p "Do you want to commit these changes now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        read -p "Enter commit message: " commit_message
        git commit -m "$commit_message"
        print_success "Changes committed"
    fi
fi

# Step 7: Check for remote repository
echo ""
print_status "Checking git remote..."
if git remote -v | grep -q 'origin'; then
    print_success "Git remote 'origin' configured"
    git remote -v
else
    print_warning "No git remote configured"
    echo ""
    print_warning "You need to push your code to GitHub/GitLab/Bitbucket before deploying to Render."
    echo ""
    read -p "Do you want to add a remote now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your remote repository URL: " remote_url
        git remote add origin "$remote_url"
        print_success "Remote added"
    fi
fi

# Step 8: Offer to push to remote
echo ""
if git remote -v | grep -q 'origin'; then
    read -p "Do you want to push to your remote repository now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Pushing to remote..."
        git push -u origin main 2>/dev/null || git push -u origin master
        if [ $? -eq 0 ]; then
            print_success "Code pushed to remote"
        else
            print_error "Failed to push. You may need to set up your remote or resolve conflicts."
        fi
    fi
fi

# Step 9: Summary and next steps
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "   ✅ PRE-DEPLOYMENT CHECKS COMPLETE"
echo "════════════════════════════════════════════════════════════════"
echo ""
print_success "Your project is ready for Render deployment!"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Go to: ${BLUE}https://dashboard.render.com${NC}"
echo "2. Click: ${BLUE}New → Blueprint${NC}"
echo "3. Connect your repository"
echo "4. Render will detect ${BLUE}render.yaml${NC} automatically"
echo "5. Set these environment variables:"
echo "   - ${YELLOW}GROQ_API_KEY${NC} (from https://console.groq.com/keys)"
echo "   - ${YELLOW}CALCOM_API_KEY${NC} (from https://app.cal.com/settings/developer)"
echo "   - ${YELLOW}CALCOM_EVENT_TYPE_ID${NC} (your event type ID)"
echo "   - ${YELLOW}CALCOM_USERNAME${NC} (your Cal.com username)"
echo "6. Click ${BLUE}Apply${NC} to deploy"
echo ""
echo "📚 DOCUMENTATION:"
echo "   - Quick Start: ${BLUE}RENDER_QUICKSTART.md${NC}"
echo "   - Full Guide: ${BLUE}DEPLOYMENT.md${NC}"
echo "   - Checklist: ${BLUE}DEPLOYMENT_CHECKLIST.md${NC}"
echo "   - Summary: ${BLUE}RENDER_DEPLOYMENT_SUMMARY.md${NC}"
echo ""
echo "⏱️  Estimated deployment time: 5-10 minutes"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
print_success "Good luck with your deployment! 🚀"
echo ""

