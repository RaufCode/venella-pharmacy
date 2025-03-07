const express = require('express');
const { authenticate, authorize } = require('../middleware/auth');

const router = express.Router();

// Example of a protected route for admin only
router.get('/admin', authenticate, authorize(['admin']), (req, res) => {
    res.json({ message: `Hello Admin ${req.user.first_name}` });
});

// Example of a protected route for salespersons and admins
router.get('/sales', authenticate, authorize(['salesperson', 'admin']), (req, res) => {
    res.json({ message: `Hello Salesperson/Admin ${req.user.first_name}` });
});

// Example of a protected route for all roles
router.get('/dashboard', authenticate, (req, res) => {
    res.json({ message: `Welcome to your dashboard, ${req.user.first_name}!` });
});

module.exports = router;
