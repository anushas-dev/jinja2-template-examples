#!/usr/bin/env python3
"""
Dynamic Email Template Renderer for TechFlow Solutions
====================================================

This script renders the email newsletter template with dynamic content
using Jinja2 templating engine. It supports:

- Dynamic content loading from JSON data files
- Personalization based on user data
- Multiple template variants (Hacktoberfest, regular newsletter, etc.)
- Email preview generation
- Batch rendering for multiple recipients

Usage:
    python email_renderer.py                    # Render with default data
    python email_renderer.py --user-data user.json  # Render with custom user data
    python email_renderer.py --preview         # Open preview in browser
    python email_renderer.py --variant hacktoberfest  # Use specific variant
"""

import json
import os
import sys
import argparse
import webbrowser
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict, Any, Optional

class EmailRenderer:
    """Email template renderer with dynamic content support."""
    
    def __init__(self, base_dir: Optional[str] = None):
        """Initialize the email renderer.
        
        Args:
            base_dir: Base directory for templates. Defaults to current script directory.
        """
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.templates_dir = self.base_dir / "templates"
        
        # Setup Jinja2 environment with autoescape for security
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['format_date'] = self._format_date
        self.env.filters['truncate_words'] = self._truncate_words
        
    def _format_date(self, date_str: str, format_type: str = "month_year") -> str:
        """Custom Jinja2 filter to format dates."""
        try:
            if format_type == "month_year":
                date_obj = datetime.strptime(date_str, "%Y-%m")
                return date_obj.strftime("%B %Y")
            elif format_type == "full_date":
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                return date_obj.strftime("%B %d, %Y")
            return date_str
        except ValueError:
            return date_str
    
    def _truncate_words(self, text: str, count: int = 20) -> str:
        """Custom Jinja2 filter to truncate text by word count."""
        words = text.split()
        if len(words) <= count:
            return text
        return ' '.join(words[:count]) + '...'
    
    def load_data(self, data_file: str = "email-data.json") -> Dict[str, Any]:
        """Load email data from JSON file.
        
        Args:
            data_file: Name of the JSON data file in templates directory.
            
        Returns:
            Dictionary containing email data.
            
        Raises:
            FileNotFoundError: If data file doesn't exist.
            json.JSONDecodeError: If JSON is invalid.
        """
        data_path = self.templates_dir / data_file
        
        if not data_path.exists():
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Add dynamic current year if not specified
            if 'current_year' not in data:
                data['current_year'] = datetime.now().year
                
            return data
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in {data_file}: {e}")
    
    def load_user_data(self, user_file: str) -> Dict[str, Any]:
        """Load personalized user data.
        
        Args:
            user_file: Path to user-specific JSON file.
            
        Returns:
            Dictionary containing user personalization data.
        """
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: User data file {user_file} not found. Using defaults.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {user_file}: {e}. Using defaults.")
            return {}
    
    def merge_data(self, base_data: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Merge base template data with user-specific personalization.
        
        Args:
            base_data: Base template data.
            user_data: User-specific personalization data.
            
        Returns:
            Merged data dictionary.
        """
        merged = base_data.copy()
        
        # Add user personalization
        if user_data:
            merged['user'] = user_data
            
            # Personalize greeting if user name is provided
            if 'name' in user_data:
                company_name = merged.get('company', {}).get('name', 'TechFlow Solutions')
                merged['newsletter']['greeting'] = f"Hello {user_data['name']}, welcome back to {company_name}"
            
            # Customize recommendations based on user preferences
            if 'interests' in user_data:
                self._customize_content_for_interests(merged, user_data['interests'])
        
        return merged
    
    def _customize_content_for_interests(self, data: Dict[str, Any], interests: list) -> None:
        """Customize content based on user interests.
        
        Args:
            data: Email data to modify.
            interests: List of user interests.
        """
        # Example: Reorder articles based on interests
        if 'articles' in data and interests:
            articles = data['articles']
            prioritized = []
            remaining = []
            
            for article in articles:
                # Simple keyword matching (in real app, you'd use more sophisticated matching)
                if any(interest.lower() in article['title'].lower() or 
                      interest.lower() in article['description'].lower() 
                      for interest in interests):
                    prioritized.append(article)
                else:
                    remaining.append(article)
            
            data['articles'] = prioritized + remaining
    
    def render_template(self, template_name: str, data: Dict[str, Any]) -> str:
        """Render email template with provided data.
        
        Args:
            template_name: Name of the Jinja2 template file.
            data: Data dictionary for template rendering.
            
        Returns:
            Rendered HTML email as string.
            
        Raises:
            TemplateNotFound: If template file doesn't exist.
        """
        template = self.env.get_template(template_name)
        return template.render(**data)
    
    def save_rendered_email(self, html_content: str, output_file: str = "rendered_email.html") -> Path:
        """Save rendered email to HTML file.
        
        Args:
            html_content: Rendered HTML content.
            output_file: Output filename.
            
        Returns:
            Path to saved file.
        """
        output_path = self.base_dir / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def render_email(self, 
                    template_name: str = "email-template.j2",
                    data_file: str = "email-data.json",
                    user_data_file: Optional[str] = None,
                    output_file: str = "rendered_email.html") -> Path:
        """Complete email rendering workflow.
        
        Args:
            template_name: Jinja2 template filename.
            data_file: JSON data filename.
            user_data_file: Optional user personalization data file.
            output_file: Output HTML filename.
            
        Returns:
            Path to rendered email file.
        """
        # Load base data
        print(f"📧 Loading email data from {data_file}...")
        base_data = self.load_data(data_file)
        
        # Load user data if provided
        user_data = {}
        if user_data_file:
            print(f"👤 Loading user data from {user_data_file}...")
            user_data = self.load_user_data(user_data_file)
        
        # Merge data
        print("🔄 Merging template data...")
        merged_data = self.merge_data(base_data, user_data)
        
        # Render template
        print(f"🎨 Rendering template {template_name}...")
        html_content = self.render_template(template_name, merged_data)
        
        # Save output
        output_path = self.save_rendered_email(html_content, output_file)
        print(f"✅ Email rendered successfully: {output_path}")
        
        return output_path

def create_sample_user_data():
    """Create sample user data files for demonstration."""
    base_dir = Path(__file__).parent
    templates_dir = base_dir / "templates"
    
    # Sample user data
    sample_users = [
        {
            "name": "Alex Chen",
            "email": "alex.chen@example.com",
            "interests": ["automation", "productivity", "open source"],
            "plan": "pro",
            "signup_date": "2024-03-15",
            "last_activity": "2025-10-10"
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.j@company.com",
            "interests": ["team management", "scaling", "performance"],
            "plan": "enterprise",
            "signup_date": "2023-11-20",
            "last_activity": "2025-10-14"
        }
    ]
    
    for i, user in enumerate(sample_users, 1):
        user_file = templates_dir / f"user_{i}_data.json"
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user, f, indent=2)
        print(f"📝 Created sample user data: {user_file}")

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Render dynamic email templates with Jinja2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python email_renderer.py                           # Basic rendering
  python email_renderer.py --preview                 # Render and open in browser
  python email_renderer.py --user-data user_1_data.json  # Personalized email
  python email_renderer.py --create-samples          # Create sample user data files
  python email_renderer.py --template custom.j2      # Use custom template
        """
    )
    
    parser.add_argument(
        "--template", "-t",
        default="email-template.j2",
        help="Template filename (default: email-template.j2)"
    )
    
    parser.add_argument(
        "--data", "-d",
        default="email-data.json",
        help="Data filename (default: email-data.json)"
    )
    
    parser.add_argument(
        "--user-data", "-u",
        help="User personalization data file"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="rendered_email.html",
        help="Output filename (default: rendered_email.html)"
    )
    
    parser.add_argument(
        "--preview", "-p",
        action="store_true",
        help="Open rendered email in default browser"
    )
    
    parser.add_argument(
        "--create-samples",
        action="store_true",
        help="Create sample user data files"
    )
    
    args = parser.parse_args()
    
    try:
        # Create sample files if requested
        if args.create_samples:
            create_sample_user_data()
            return
        
        # Initialize renderer
        renderer = EmailRenderer()
        
        # Render email
        output_path = renderer.render_email(
            template_name=args.template,
            data_file=args.data,
            user_data_file=args.user_data,
            output_file=args.output
        )
        
        # Open preview if requested
        if args.preview:
            print(f"🌐 Opening preview in browser...")
            webbrowser.open(f"file://{output_path.absolute()}")
        
        print(f"\n🎉 Email rendering complete!")
        print(f"📄 Output file: {output_path}")
        print(f"🔗 Preview URL: file://{output_path.absolute()}")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()