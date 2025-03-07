const jwt = require('jsonwebtoken');
const { User } = require('../models');

// Middleware to verify the token and attach user info
const authenticate = async (req, res, next) => {
    const token = req.header('Authorization')?.split(' ')[1];
    if (!token) {
        return res.status(401).json({ message: 'Access denied. No token provided.' });
    }

    try {
        const decoded = jwt.verify(token, 'secretkey');
        const user = await User.findByPk(decoded.id);

        if (!user) {
            return res.status(404).json({ message: 'User not found.' });
        }

        req.user = user; // Attach user info to the request object
        next();
    } catch (error) {
        res.status(401).json({ message: 'Invalid token.' });
    }
};

// Middleware to check user roles
const authorize = (roles) => {
    return (req, res, next) => {
        if (!roles.includes(req.user.role)) {
            return res.status(403).json({ message: 'Access denied. Insufficient permissions.' });
        }
        next();
    };
};

module.exports = { authenticate, authorize };
