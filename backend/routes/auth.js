const express = require('express');
const { body, validationResult } = require('express-validator');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { User } = require('../models');

const router = express.Router();


router.post(
    '/register',
    [
        body('first_name').notEmpty().withMessage('First name is required'),
        body('last_name').notEmpty().withMessage('Last name is required'),
        body('email').isEmail().withMessage('Valid email is required'),
        body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters long'),
        body('role').isIn(['customer', 'salesperson', 'admin']).withMessage('Invalid role'),
    ],
    async (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }
        console.log(req.body)
        const { first_name, last_name, email, password, role } = req.body;
        console.log({ first_name, last_name, email, password, role })

        try {

            // Check if the user already exists
            const existingUser = await User.findOne({ where: { email } })
            if (existingUser) {
                return res.status(400).json({ message: 'User already exists' });
            }

            // Hash the password
            const hashedPassword = await bcrypt.hash(password, 10);

            // Create a new user
            const user = await User.create({ first_name, last_name, email, password: hashedPassword, role })

            res.status(201).json({ message: 'User registered successfully' });

        } catch (error) {
            res.status(500).json({ message: 'Server error', error: error.message })
        }
    }
);

// Login Route
router.post(
    '/login',
    [
        body('email').isEmail().withMessage('Valid email is required'),
        body('password').notEmpty().withMessage('Password is required'),
    ],
    async (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { email, password } = req.body;

        try {

            const user = await User.findOne({ where: { email } })
            if (!user) {
                return res.status(400).json({ message: 'Invalid credentials' });
            }

            const isMatch = await bcrypt.compare(password, user.password);
            if (!isMatch) {
                return res.status(400).json({ message: 'Incorrect password' });
            }

            const token = jwt.sign({ id: user.id, role: user.role }, 'secretkey', { expiresIn: '1h' });

            res.json({ token, user });

        } catch (error) {
            res.status(500).json({ message: 'Server error', error: error.message });
        }

    }
);

module.exports = router;
