require('dotenv').config();
const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const dbConfig = {
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  waitForConnections: true,
  connectionLimit: 10
};

let pool;

async function initDB() {
  pool = mysql.createPool(dbConfig);
  await pool.execute(`
    CREATE TABLE IF NOT EXISTS tasks (
      id INT AUTO_INCREMENT PRIMARY KEY,
      title VARCHAR(255) NOT NULL,
      description TEXT,
      status ENUM('todo', 'in_progress', 'done') DEFAULT 'todo',
      priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
  `);
  console.log('Database initialized');
}

// Health check
app.get('/health', async (req, res) => {
  try {
    await pool.execute('SELECT 1');
    res.json({ status: 'healthy', database: 'connected', timestamp: new Date().toISOString() });
  } catch (err) {
    res.status(500).json({ status: 'unhealthy', database: 'disconnected', error: err.message });
  }
});

// DB info
app.get('/api/db-info', async (req, res) => {
  try {
    const [rows] = await pool.execute('SELECT VERSION() as version, DATABASE() as db_name');
    res.json({ host: process.env.DB_HOST, ...rows[0] });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get all tasks
app.get('/api/tasks', async (req, res) => {
  try {
    const [rows] = await pool.execute('SELECT * FROM tasks ORDER BY created_at DESC');
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Create task
app.post('/api/tasks', async (req, res) => {
  const { title, description, priority = 'medium' } = req.body;
  if (!title) return res.status(400).json({ error: 'Title is required' });
  try {
    const [result] = await pool.execute(
      'INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)',
      [title, description || '', priority]
    );
    const [rows] = await pool.execute('SELECT * FROM tasks WHERE id = ?', [result.insertId]);
    res.status(201).json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Update task status
app.patch('/api/tasks/:id', async (req, res) => {
  const { status, title, description, priority } = req.body;
  try {
    await pool.execute(
      'UPDATE tasks SET status = COALESCE(?, status), title = COALESCE(?, title), description = COALESCE(?, description), priority = COALESCE(?, priority) WHERE id = ?',
      [status || null, title || null, description || null, priority || null, req.params.id]
    );
    const [rows] = await pool.execute('SELECT * FROM tasks WHERE id = ?', [req.params.id]);
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Delete task
app.delete('/api/tasks/:id', async (req, res) => {
  try {
    await pool.execute('DELETE FROM tasks WHERE id = ?', [req.params.id]);
    res.json({ message: 'Task deleted' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Stats
app.get('/api/stats', async (req, res) => {
  try {
    const [total] = await pool.execute('SELECT COUNT(*) as count FROM tasks');
    const [byStatus] = await pool.execute('SELECT status, COUNT(*) as count FROM tasks GROUP BY status');
    const [byPriority] = await pool.execute('SELECT priority, COUNT(*) as count FROM tasks GROUP BY priority');
    res.json({ total: total[0].count, byStatus, byPriority });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

initDB().then(() => {
  app.listen(3000, () => console.log('Server running on port 3000'));
});