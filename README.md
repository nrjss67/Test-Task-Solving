# Social Media API

A Django-based social media platform with REST API support, featuring user authentication, posts, likes, and hashtags.

## Features

- User authentication with email
- User profiles with profile pictures and bio
- Post creation with images and text
- Like system for posts
- Hashtag support
- Follow/Unfollow functionality
- REST API endpoints
- Celery for background tasks
- JWT authentication

## Tech Stack

- Python 3.x
- Django 5.2
- Django REST Framework
- Celery
- Redis
- PostgreSQL (recommended)
- Pillow for image handling

## Prerequisites

- Python 3.x
- pip
- Redis server
- Virtual environment (recommended)
- Docker and Docker Compose (for Docker installation)

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd social-media-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Start Redis server:
```bash
redis-server
```

8. Start Celery worker:
```bash
celery -A social_media worker -l info
```

9. Run the development server:
```bash
python manage.py runserver
```

### Docker Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd social-media-api
```

2. Create a `.env` file in the root directory with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres@db:5432/social_media
REDIS_URL=redis://redis:6379/0
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. In a new terminal, run migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Create superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

The application will be available at:
- Web: http://localhost:8000
- API Documentation: http://localhost:8000/api/schema/swagger-ui/

To stop the containers:
```bash
docker-compose down
```

To view logs:
```bash
docker-compose logs -f
```

## API Endpoints

### Authentication
- POST /api/token/ - Get JWT token
- POST /api/token/refresh/ - Refresh JWT token

### Users
- GET /api/users/ - List users
- POST /api/users/ - Create user
- GET /api/users/{id}/ - Get user details
- PUT /api/users/{id}/ - Update user
- DELETE /api/users/{id}/ - Delete user

### Posts
- GET /api/posts/ - List posts
- POST /api/posts/ - Create post
- GET /api/posts/{id}/ - Get post details
- PUT /api/posts/{id}/ - Update post
- DELETE /api/posts/{id}/ - Delete post

### Likes
- POST /api/posts/{id}/like/ - Like a post
- DELETE /api/posts/{id}/like/ - Unlike a post

### Hashtags
- GET /api/hashtags/ - List hashtags
- GET /api/hashtags/{id}/ - Get hashtag details

## Project Structure

```
social_media/
├── social_media/          # Main project directory
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── social_media_service/  # Main app directory
│   ├── models.py         # Database models
│   ├── views.py          # API views
│   ├── serializers.py    # API serializers
│   └── urls.py           # App URL configuration
├── user/                 # User app directory
│   ├── models.py         # User models
│   └── views.py          # User views
└── requirements.txt      # Project dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 