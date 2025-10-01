# DocCollab - Collaborative LaTeX Editor

A collaborative LaTeX editor built with Flask, featuring real-time editing, PDF compilation, and multi-language support.

## Features

- 🔐 User authentication and authorization
- 📝 Real-time LaTeX editing with CodeMirror
- 📄 PDF compilation and viewing
- 🌍 Multi-language support (EN, PT, ES)
- 📁 Project management
- 💾 Auto-save functionality
- 🎨 Modern Bootstrap UI

## Tech Stack

- **Backend:** Flask, SQLAlchemy, Flask-Login
- **Frontend:** Bootstrap 5, CodeMirror, JavaScript
- **Database:** SQLite
- **LaTeX:** pdflatex
- **i18n:** Flask-Babel

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/seuusuario/doccollab.git
   cd doccollab
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Initialize database:**
   ```bash
   python setup_db.py
   ```

6. **Run the application:**
   ```bash
   python app.py
   ```

### Deploy to Cloud

#### Replit
1. Import this repository to Replit
2. Configure environment variables
3. Run the application

#### PythonAnywhere
1. Upload files to PythonAnywhere
2. Configure WSGI file
3. Set up environment variables

#### Heroku
1. Connect GitHub repository
2. Configure environment variables
3. Deploy automatically

## Environment Variables

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///doccollab.db
PDFLATEX=/usr/bin/pdflatex
SEED_EMAIL=admin@example.com
SEED_PASSWORD=admin123
```

## Default Login

- **Email:** admin@example.com
- **Password:** admin123

## Project Structure

```
doccollab/
├── app.py                 # Main Flask application
├── wsgi.py               # WSGI entry point
├── requirements.txt      # Python dependencies
├── models/               # Database models
├── routes/               # Flask routes
├── services/             # Business logic
├── utils/                # Utility functions
├── templates/            # HTML templates
├── static/               # CSS, JS, images
└── translations/         # i18n files
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For support, email support@doccollab.com or create an issue on GitHub.


