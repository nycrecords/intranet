# Dynamic Announcement Management Implementation

## Overview
Successfully implemented a complete dynamic announcement management system for the DORIS intranet homepage. This allows administrators to easily update the three announcement cards without modifying code directly.

## Implementation Summary

### ✅ Completed Features

#### 1. Database Model (`app/models.py`)
- **AnnouncementCard** model with fields:
  - `id` (Primary Key)
  - `title` (String, 255 chars)
  - `link` (String, 500 chars)
  - `image_filename` (String, 255 chars)
  - `is_active` (Boolean, default=True)
  - `display_order` (Integer, 1-3)
  - `created_at` & `updated_at` (DateTime)
- **Class methods**: `get_active_announcements()`, `populate_defaults()`
- **Properties**: `image_url` for consistent path handling

#### 2. Database Migration (`migrations/versions/abc123456789_add_announcement_cards_table.py`)
- Creates `announcement_cards` table
- Pre-populates with current hardcoded announcements
- Includes proper upgrade/downgrade functions

#### 3. Form Handling (`app/main/forms.py`)
- **AnnouncementForm** with:
  - 3 sets of title, link, and image upload fields
  - Save, Preview, and Reset buttons
  - Proper validation (DataRequired, Length constraints)
  - File upload support with size/type validation

#### 4. Admin Routes (`app/main/views.py`)
- **`/admin/announcements`** - Main admin interface
  - Login required with admin permission check
  - GET: Displays current announcements in form
  - POST: Processes save/reset operations
  - Secure file upload handling
  - Error handling with flash messages

- **`/admin/announcements/preview`** - AJAX preview endpoint
  - Real-time preview functionality
  - Secure admin-only access
  - Returns rendered HTML for preview

- **Permission system**: Uses existing roles (Administrator, Super User)

#### 5. Admin Template (`app/templates/admin_announcements.html`)
- Responsive Bootstrap-based design
- Three announcement card editors
- Real-time preview section
- File upload with current image display
- JavaScript-powered preview functionality
- Flash message support
- Form validation feedback

#### 6. Homepage Integration
- **Modified `homepage_hero/homepage_hero.html`**:
  - Dynamic data loading from database
  - Fallback to hardcoded announcements
  - Smart link handling (internal vs external)
  - Image path management

- **Updated `index` view**:
  - Loads active announcements
  - Passes data to template
  - Maintains existing functionality

#### 7. File Management
- **Upload directory**: `/static/uploads/announcements/`
- **Security**: Secure filename handling with timestamps
- **Validation**: JPG/PNG file type checking
- **Storage**: Organized file structure

#### 8. Styling & UX
- **Custom CSS**: `admin_announcements.css`
- **Responsive design**: Mobile-friendly interface
- **Visual feedback**: Hover effects, loading states
- **Consistent theming**: Matches existing DORIS design

## How to Use

### Access the Admin Interface
1. Log in as Administrator or Super User
2. Navigate to `/admin/announcements`
3. Edit the three announcement cards
4. Use "Preview" to see changes before saving
5. Click "Save Changes" to update the homepage
6. Use "Reset to Defaults" to restore original announcements

### File Uploads
- Supported formats: JPG, PNG
- Recommended size: Under 5MB
- Images are automatically renamed with timestamps
- Current images are displayed for reference

### Preview Feature
- Real-time preview shows exactly how announcements will appear
- No need to save changes to see the preview
- Preview updates immediately when clicking the Preview button

## Technical Details

### Security Features
- Admin-only access with role verification
- Secure file upload handling
- CSRF protection on all forms
- Input validation and sanitization
- Path traversal protection

### Database Design
- Efficient querying with indexed display_order
- Soft deletion capability with is_active flag
- Automatic timestamp management
- Migration includes default data population

### Error Handling
- Comprehensive error catching in upload process
- User-friendly error messages
- Database rollback on failures
- Flash message system for feedback

### Performance Considerations
- Minimal database queries (single query for announcements)
- Optimized image serving
- Cached template rendering
- Efficient file upload processing

## File Structure
```
app/
├── models.py (+ AnnouncementCard model)
├── main/
│   ├── forms.py (+ AnnouncementForm)
│   └── views.py (+ admin routes, updated index)
├── templates/
│   ├── admin_announcements.html (new)
│   └── homepage_hero/
│       └── homepage_hero.html (modified)
└── static/
    ├── css/
    │   └── admin_announcements.css (new)
    └── uploads/
        └── announcements/ (new directory)

migrations/versions/
└── abc123456789_add_announcement_cards_table.py (new)
```

## Next Steps for Production Deployment

1. **Run Database Migration**:
   ```bash
   flask db upgrade
   ```

2. **Set Proper File Permissions**:
   ```bash
   chmod 755 app/static/uploads/announcements
   ```

3. **Configure Web Server**:
   - Ensure upload directory is accessible
   - Set appropriate file size limits
   - Configure backup strategy for uploaded images

4. **Test Admin Access**:
   - Verify admin users can access the interface
   - Test file upload functionality
   - Confirm preview feature works correctly

## Maintenance Notes

- **Image Cleanup**: Consider implementing a cleanup process for unused images
- **Backup Strategy**: Include uploaded images in backup procedures
- **Monitoring**: Monitor upload directory disk usage
- **Updates**: Future updates should maintain the AnnouncementCard model structure

This implementation provides a complete, production-ready solution for dynamic announcement management while maintaining backward compatibility and security best practices.