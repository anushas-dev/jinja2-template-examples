#!/usr/bin/env python3
"""
Batch Email Renderer
===================

This script demonstrates batch rendering of personalized emails
for multiple users using the EmailRenderer class.

Usage:
    python batch_render.py
"""

import os
from pathlib import Path
from email_renderer import EmailRenderer

def batch_render_emails():
    """Render emails for all sample users."""
    renderer = EmailRenderer()
    base_dir = Path(__file__).parent
    templates_dir = base_dir / "templates"
    
    # Find all user data files
    user_files = list(templates_dir.glob("user_*_data.json"))
    
    if not user_files:
        print("❌ No user data files found. Run with --create-samples first.")
        return
    
    print(f"🚀 Starting batch rendering for {len(user_files)} users...\n")
    
    rendered_files = []
    
    for user_file in user_files:
        try:
            # Extract user identifier from filename
            user_id = user_file.stem.replace("_data", "")
            output_file = f"batch_rendered_{user_id}.html"
            
            print(f"👤 Rendering email for {user_file.name}...")
            
            # Render personalized email
            output_path = renderer.render_email(
                user_data_file=str(user_file),
                output_file=output_file
            )
            
            rendered_files.append(output_path)
            print(f"✅ Saved: {output_path}\n")
            
        except Exception as e:
            print(f"❌ Error rendering {user_file}: {e}\n")
    
    print(f"🎉 Batch rendering complete!")
    print(f"📧 Rendered {len(rendered_files)} emails:")
    for file_path in rendered_files:
        print(f"   • {file_path}")

def demo_advanced_features():
    """Demonstrate advanced features of the email renderer."""
    print("🎨 Advanced Email Rendering Demo\n")
    
    renderer = EmailRenderer()
    
    # Load base data and show customization
    data = renderer.load_data()
    
    print("📊 Template Data Structure:")
    print(f"   • Company: {data['company']['name']}")
    print(f"   • Newsletter: {data['newsletter']['title']} ({data['newsletter']['date']})")
    print(f"   • Articles: {len(data['articles'])} featured articles")
    print(f"   • Feature: {data['feature']['title']}")
    print(f"   • Promo Code: {data['promo']['code']}")
    print()
    
    # Show user personalization
    user_files = list(Path("templates").glob("user_*_data.json"))
    
    for user_file in user_files[:2]:  # Show first 2 users
        user_data = renderer.load_user_data(str(user_file))
        print(f"👤 User: {user_data.get('name', 'Unknown')}")
        print(f"   • Email: {user_data.get('email', 'N/A')}")
        print(f"   • Plan: {user_data.get('plan', 'N/A')}")
        print(f"   • Interests: {', '.join(user_data.get('interests', []))}")
        print()

if __name__ == "__main__":
    demo_advanced_features()
    batch_render_emails()