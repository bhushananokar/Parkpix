const express = require('express');
const bodyParser = require('body-parser');
const admin = require('firebase-admin');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

// Ensure uploads directory exists
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
  console.log('Uploads directory created');
}

// Initialize Firebase Admin SDK
const serviceAccount = require('./'); // your firebase admin sdk 

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  storageBucket: 'Your-project-id.appspot.com'
});

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/upload', upload.single('image'), (req, res) => {
  const file = req.file;
  if (!file) {
    console.error('No file received');
    return res.status(400).send('No file received');
  }

  const bucket = admin.storage().bucket();
  const uploadOptions = {
    destination: `images/${file.filename}.jpg`,
    metadata: {
      contentType: 'image/jpeg',
    },
  };

  console.log('Received file:', file);
  console.log('File path:', file.path);

  bucket.upload(file.path, uploadOptions, (err, uploadedFile) => {
    if (err) {
      console.error('Error uploading file:', err);
      return res.status(500).send('Error uploading file');
    }

    console.log('File uploaded successfully:', uploadedFile.name);

    // Remove the file from the local server
    fs.unlink(file.path, (unlinkErr) => {
      if (unlinkErr) {
        console.error('Error deleting file:', unlinkErr);
      } else {
        console.log('File deleted successfully from local server');
      }
    });

    res.status(200).send('File uploaded successfully');
  });
});

// Test endpoint to verify file writing
app.get('/test-upload', (req, res) => {
  const testFilePath = path.join(uploadsDir, 'test.txt');
  fs.writeFile(testFilePath, 'This is a test file', (err) => {
    if (err) {
      console.error('Error writing test file:', err);
      return res.status(500).send('Error writing test file');
    }
    console.log('Test file written successfully');
    res.status(200).send('Test file written successfully');
  });
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
