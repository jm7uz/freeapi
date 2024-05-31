const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(bodyParser.json());

app.post('/api/video-watched', (req, res) => {
    const watchData = req.body;
    console.log(watchData);
    res.json({ message: 'Data scanning...' });
});

app.get('/', (req, res) => {
    res.json({ message: 'hello' });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
