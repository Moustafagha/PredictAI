from flask import Blueprint, request, jsonify
from user import db, User

# Create blueprint
user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'data': [user.to_dict() for user in users]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['username', 'email']):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: username, email'
            }), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'Username already exists'
            }), 400
        
        existing_email = User.query.filter_by(email=data['email']).first()
        if existing_email:
            return jsonify({
                'success': False,
                'error': 'Email already exists'
            }), 400
        
        # Create new user
        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500