# 🎒 Pocket-Git

> A minimal git implementation that fits in your pocket!

[![PyPI version](https://badge.fury.io/py/pocket-git.svg)](https://badge.fury.io/py/pocket-git)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

```bash
# Install
pip install pocket-git

# Use it!
pocket-git init
pocket-git add myfile.txt
pocket-git commit "My first commit"
pocket-git log
```

Or use the shorter alias:

```bash
pgit init
pgit add myfile.txt
pgit commit "First commit"
```

## ✨ Features

- ✅ `init` - Initialize repository
- ✅ `add` - Stage files for commit
- ✅ `commit` - Create snapshots of your project
- ✅ `log` - View commit history
- ✅ `status` - Check what's staged

## 📚 What You'll Learn

Pocket-Git implements the core concepts that make git work:

### Content-Addressable Storage

Every file is stored as a "blob" object, identified by its SHA-1 hash. Same content = same hash = stored once!

### The Three Trees

1. **Working Directory** - Your actual files
2. **Staging Area (Index)** - Files prepared for commit
3. **Repository (.pocket-git/)** - Committed snapshots

### Object Model

- **Blobs** - File contents
- **Trees** - Directory structures
- **Commits** - Snapshots with metadata and parent links

### DAG (Directed Acyclic Graph)

Commits form a chain, each pointing to its parent, creating your project's history.

## 🔍 How It Works

```bash
# When you run 'pocket-git add file.txt':
1. File content is read
2. SHA-1 hash is calculated
3. Content is compressed and stored in .pocket-git/objects/
4. Filename → hash mapping added to staging area

# When you run 'pocket-git commit "message"':
1. Tree object created from staging area
2. Commit object created with:
   - Reference to tree
   - Parent commit
   - Author and timestamp
   - Your message
3. Branch reference updated to point to new commit
```

## 📖 Tutorial

### Initialize a Repository

```bash
mkdir my-project
cd my-project
pocket-git init
```

This creates `.pocket-git/` with:

- `objects/` - where all content is stored
- `refs/heads/` - branch pointers
- `HEAD` - points to current branch
- `index` - staging area

### Make Your First Commit

```bash
echo "Hello World" > hello.txt
pocket-git add hello.txt
pocket-git status
pocket-git commit "Add hello.txt"
```

### View History

```bash
pocket-git log
```

### Explore the Internals

```bash
# See the objects created
ls -la .pocket-git/objects/

# Objects are named by their hash
# Try decompressing one to see the content!
```

## 🛠️ Development

```bash
# Clone the repo
git clone https://github.com/yourusername/pocket-git.git
cd pocket-git

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Make changes and test
pgit init
pgit add test.txt
pgit commit "Testing my changes"
```

## 🤝 Contributing

Contributions welcome! This is a learning project, so:

- Keep code simple and well-commented
- Explain _why_, not just _what_
- Add tests for new features
- Update documentation

⭐ Star this repo if you learned something new!
