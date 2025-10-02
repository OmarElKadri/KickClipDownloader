# Overview

This is a Flask-based web application that allows users to download video clips from Kick.com. The application uses yt-dlp (a youtube-dl fork) to fetch and download video content. Users can paste a Kick clip URL through a web interface, and the application handles the download process, merging video and audio streams into a single MP4 file.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture

**Single-Page Application (SPA) Pattern**
- Uses vanilla HTML/CSS with inline styles for simplicity
- No frontend framework dependencies (React, Vue, etc.)
- Likely uses JavaScript fetch API for AJAX requests to the backend
- Gradient-based modern UI design with centered layout

**Rationale**: Keeps the application lightweight and eliminates build steps. For a simple utility like a video downloader, a full frontend framework would be overkill.

## Backend Architecture

**Flask Microframework**
- Minimalist Python web framework
- Session management using Flask's built-in session handling with a secret key
- RESTful API design with JSON responses
- Stateless request handling

**Rationale**: Flask is ideal for small to medium applications that don't require the complexity of Django. It provides just enough structure without being opinionated about architecture.

**File Download Management**
- Downloads stored in a local `downloads/` directory
- Files are created on-demand and likely served temporarily
- Path library used for cross-platform file path handling

**Design Decision**: Local file storage is simple but not scalable for multi-user concurrent scenarios. Consider cloud storage (S3, etc.) for production deployment with high traffic.

## Media Processing

**yt-dlp Integration**
- yt-dlp handles all video extraction and download logic
- Configured to merge best video and audio streams automatically
- Output format standardized to MP4 for universal compatibility
- Error handling wrapped around yt-dlp operations

**Rationale**: yt-dlp is the most robust and actively maintained tool for downloading videos from streaming platforms. It handles format detection, stream merging, and platform-specific quirks automatically.

**Configuration Options**:
- `format: 'bestvideo+bestaudio/best'` - Prioritizes quality
- `merge_output_format: 'mp4'` - Ensures compatibility
- `noplaylist: True` - Prevents accidental bulk downloads
- `quiet: True` and `no_warnings: True` - Cleaner error handling

## Session Management

**Flask Sessions**
- Secret key loaded from environment variable with fallback to random generation
- Used for potential user-specific download tracking or rate limiting

**Security Consideration**: The secret key should always come from environment variables in production, not the fallback random generation (which changes on restart).

## Error Handling

**Try-Catch Pattern**
- All yt-dlp operations wrapped in exception handling
- Returns structured JSON responses with success/failure status
- Errors propagated to frontend as error messages

**Rationale**: Provides graceful degradation and allows frontend to display meaningful error messages to users.

# External Dependencies

## Core Dependencies

**yt-dlp** (Primary Integration)
- Purpose: Video downloading and format conversion
- Handles all interaction with Kick.com platform
- Provides video metadata extraction
- Note: Requires periodic updates to maintain compatibility with streaming platforms

**Flask** (Web Framework)
- Purpose: HTTP request handling, routing, and templating
- Provides session management
- Serves static HTML templates

## System Dependencies

**FFmpeg** (Implicit Dependency via yt-dlp)
- Required by yt-dlp for video/audio stream merging
- Must be installed on the system PATH
- Critical for MP4 output format

## Environment Variables

**SESSION_SECRET**
- Used for Flask session encryption
- Should be set in production environment
- Falls back to random generation in development

## File System

**Local Downloads Directory**
- Path: `downloads/`
- Created automatically if not present
- Stores temporary video files

**Considerations**: No cleanup mechanism visible in the provided code. Production systems should implement:
- Automatic file cleanup after download
- Disk space monitoring
- Rate limiting per user/session