const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const authRoutes = require('./routes/auth');
const mainRoutes = require('./routes/main');

const app = express();
const PORT = 3000;

app.use(cors({
  origin: 'http://localhost:5173',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(bodyParser.json());

app.use('/api/auth', authRoutes);
app.use('/api', mainRoutes);

app.get('/', (req, res) => {
    res.send('Welcome to the Pharmacy E-commerce Backend!');
});


app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
