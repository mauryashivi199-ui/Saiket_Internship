/**
 * Shared Storage Engine for DevBlog Studio
 * Synchronizes posts, comments, likes, and bookmarks across all multi-page HTML views using localStorage.
 */

const STORAGE_KEY = "saiket_devblog_multi_posts";
const BOOKMARKS_KEY = "saiket_devblog_bookmarks";
const COMMENTS_KEY = "saiket_devblog_comments";

const DEFAULT_POSTS = [
  {
    id: 1,
    title: "The Future of Python in Modern AI & Scalable Microservices",
    slug: "future-of-python-ai-microservices",
    author: "Shivangi Maurya",
    authorAvatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80",
    category: "Artificial Intelligence",
    readTime: "4 min read",
    coverImage: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
    excerpt: "Explore how Python's robust async ecosystem and machine learning frameworks are revolutionizing backend distributed architectures in 2026.",
    content: `Python continues to solidify its position as the undisputed lingua franca of artificial intelligence, machine learning, and high-performance backend systems.

### 🚀 Why Python Remains Dominant
1. **Unrivaled AI Ecosystem**: From PyTorch to LangChain and modern agentic frameworks, the tools powering the next generation of intelligent software are natively built in Python.
2. **Asynchronous Capabilities**: Modern async frameworks like FastAPI and AsyncIO enable Python to handle thousands of concurrent I/O operations seamlessly.
3. **Developer Velocity**: Python's clean and expressive syntax allows engineers to build prototypes in hours and scale them into production services effortlessly.

### 💡 Building for Scale
When designing backend services for high-load environments, always leverage asynchronous database drivers, implement caching layers (Redis), and decouple CPU-heavy computational workloads into background worker queues.`,
    date: "Sep 15, 2026",
    likes: 38,
    views: 1420
  },
  {
    id: 2,
    title: "Mastering Client-Side LocalStorage & Offline-First Web Apps",
    slug: "mastering-localstorage-offline-first",
    author: "Alex Rivera",
    authorAvatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=120&q=80",
    category: "Web Engineering",
    readTime: "5 min read",
    coverImage: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80",
    excerpt: "Learn how modern web architectures leverage browser storage engines like LocalStorage and IndexedDB to deliver instant, lag-free user experiences.",
    content: `Building offline-first web applications is no longer an afterthought—it is a core expectation for modern web experiences.

### 📦 Understanding the Browser Storage Hierarchy
The browser offers several tiers of persistent storage:
- **LocalStorage**: Synchronous key-value storage (~5MB to 10MB capacity), perfect for user preferences, drafts, and client-side document caching.
- **IndexedDB**: Asynchronous transactional NoSQL database suitable for massive datasets, offline file caching, and complex queries.
- **SessionStorage**: Cleared automatically when the browser tab is closed.

### ⚡ Best Practices for LocalStorage
- **Data Serialization**: Always wrap JSON transformations with safe \`try/catch\` blocks.
- **Data Versioning & Migrations**: Keep schema versions inside your storage keys to avoid breaking changes when updating data structures.
- **Multi-Tab Synchronization**: Listen to the \`window.addEventListener('storage')\` event to keep multiple open browser tabs in perfect harmony.`,
    date: "Sep 18, 2026",
    likes: 24,
    views: 890
  },
  {
    id: 3,
    title: "Top 7 Design Principles for High-Converting Fintech Dashboards",
    slug: "fintech-dashboard-design-principles",
    author: "Sophia Chen",
    authorAvatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=120&q=80",
    category: "UI/UX Design",
    readTime: "3 min read",
    coverImage: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80",
    excerpt: "From visual hierarchy to clear financial calculations, discover the key visual principles that make fintech apps trustworthy and intuitive.",
    content: `Fintech applications require a unique balance of mathematical precision, visual clarity, and high user trust.

### 🎨 Key Principles for Financial Interfaces
1. **High Visual Hierarchy**: Critical numbers (like Loan EMI, Balance, and Interest) should be bold and prominent with high contrast.
2. **Instant Feedback & Sliders**: Synchronize range sliders with direct numeric inputs so users can simulate loans in real time.
3. **Color Intentionality**: Use green for growth/gains, red for expenses/debts, and deep indigo/navy for trust and stability.
4. **Data Visualization**: Complement raw tables with clean Donut charts and Area graphs to make complex amortization intuitive.`,
    date: "Sep 19, 2026",
    likes: 45,
    views: 2150
  }
];

// Initialize Storage
function initStorage() {
  if (!localStorage.getItem(STORAGE_KEY)) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_POSTS));
  }
}

// Get All Posts
function getAllPosts() {
  initStorage();
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || DEFAULT_POSTS;
  } catch (e) {
    return DEFAULT_POSTS;
  }
}

// Save All Posts
function saveAllPosts(posts) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(posts));
}

// Get Single Post by ID
function getPostById(id) {
  const posts = getAllPosts();
  return posts.find(p => p.id === parseInt(id));
}

// Create or Update Post
function savePost(postData) {
  const posts = getAllPosts();
  if (postData.id) {
    // Update
    const idx = posts.findIndex(p => p.id === parseInt(postData.id));
    if (idx !== -1) {
      posts[idx] = { ...posts[idx], ...postData };
    }
  } else {
    // Create New
    const nextId = posts.length ? Math.max(...posts.map(p => p.id)) + 1 : 1;
    const now = new Date();
    const dateStr = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    
    // Auto-calculate read time based on words
    const wordCount = (postData.content || '').split(/\s+/).length;
    const readMin = Math.max(1, Math.ceil(wordCount / 200));

    const newPost = {
      id: nextId,
      title: postData.title,
      slug: postData.title.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
      author: postData.author || "Shivangi Maurya",
      authorAvatar: postData.authorAvatar || "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80",
      category: postData.category || "General",
      readTime: `${readMin} min read`,
      coverImage: postData.coverImage || "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=800&q=80",
      excerpt: postData.content.substring(0, 150) + "...",
      content: postData.content,
      date: dateStr,
      likes: 0,
      views: 1
    };
    posts.unshift(newPost);
  }
  saveAllPosts(posts);
  return posts;
}

// Delete Post
function deletePostById(id) {
  let posts = getAllPosts();
  posts = posts.filter(p => p.id !== parseInt(id));
  saveAllPosts(posts);
  return posts;
}

// Toggle Like
function toggleLikePost(id) {
  const posts = getAllPosts();
  const post = posts.find(p => p.id === parseInt(id));
  if (post) {
    post.likes = (post.likes || 0) + 1;
    saveAllPosts(posts);
    return post.likes;
  }
  return 0;
}

// Increment Views
function incrementViews(id) {
  const posts = getAllPosts();
  const post = posts.find(p => p.id === parseInt(id));
  if (post) {
    post.views = (post.views || 0) + 1;
    saveAllPosts(posts);
  }
}

// Comments Management
function getComments(postId) {
  try {
    const allComments = JSON.parse(localStorage.getItem(COMMENTS_KEY)) || {};
    return allComments[postId] || [
      { id: 1, author: "Aarav Sharma", date: "2 days ago", text: "Great insights! Very well structured and practical." },
      { id: 2, author: "Priya Patel", date: "Yesterday", text: "Loved the breakdown of storage tiers. Thanks for sharing!" }
    ];
  } catch (e) {
    return [];
  }
}

function addComment(postId, author, text) {
  const allComments = JSON.parse(localStorage.getItem(COMMENTS_KEY)) || {};
  if (!allComments[postId]) allComments[postId] = [];
  const newComment = {
    id: Date.now(),
    author: author || "Reader",
    date: "Just now",
    text: text
  };
  allComments[postId].unshift(newComment);
  localStorage.setItem(COMMENTS_KEY, JSON.stringify(allComments));
  return allComments[postId];
}

// Bookmarks Management
function getBookmarks() {
  try {
    return JSON.parse(localStorage.getItem(BOOKMARKS_KEY)) || [];
  } catch (e) {
    return [];
  }
}

function toggleBookmark(postId) {
  let bookmarks = getBookmarks();
  const idNum = parseInt(postId);
  if (bookmarks.includes(idNum)) {
    bookmarks = bookmarks.filter(id => id !== idNum);
  } else {
    bookmarks.push(idNum);
  }
  localStorage.setItem(BOOKMARKS_KEY, JSON.stringify(bookmarks));
  return bookmarks.includes(idNum);
}

function isBookmarked(postId) {
  return getBookmarks().includes(parseInt(postId));
}
