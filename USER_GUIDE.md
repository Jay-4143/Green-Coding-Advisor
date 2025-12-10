# Green Coding Advisor - User Guide

Welcome to the Green Coding Advisor! This guide will help you get started and make the most of the platform.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Analyzing Your Code](#analyzing-your-code)
3. [Understanding Results](#understanding-results)
4. [Badges and Achievements](#badges-and-achievements)
5. [Teams and Collaboration](#teams-and-collaboration)
6. [Dashboard and Metrics](#dashboard-and-metrics)
7. [AI Chatbot](#ai-chatbot)
8. [Tips and Best Practices](#tips-and-best-practices)

## Getting Started

### Creating an Account

1. Click **"Sign Up"** on the homepage
2. Enter your email address
3. Choose a username (3-30 characters, letters, numbers, underscores, or hyphens)
4. Create a strong password (minimum 8 characters)
5. Verify your email address (check your inbox)

### Logging In

1. Click **"Login"** on the homepage
2. Enter your email and password
3. You'll receive an access token that's valid for 30 minutes
4. Use the refresh token to get a new access token when needed

## Analyzing Your Code

### Quick Analysis (No Account Required)

1. Go to the **"Submit Code"** page
2. Paste your code in the text area
3. Select the programming language
4. Click **"Analyze"**
5. View instant results without saving

### Full Analysis (Requires Account)

1. Log in to your account
2. Navigate to **"Submit Code"**
3. Paste your code or upload a file
4. Select the language and optional project
5. Click **"Submit"**
6. Results are saved to your history

### Supported Languages

- **Python** - Full support with optimization suggestions
- **JavaScript/TypeScript** - Performance and memory optimizations
- **Java** - JVM-specific optimizations
- **C/C++** - Low-level performance analysis

## Understanding Results

### Green Score

The **Green Score** (0-100) measures your code's sustainability:
- **90-100**: Excellent - Highly optimized, minimal resource usage
- **70-89**: Good - Well-optimized with minor improvements possible
- **50-69**: Fair - Some optimization opportunities
- **0-49**: Needs Improvement - Significant optimization needed

### Metrics Explained

- **Energy Consumption (Wh)**: Estimated energy usage when running the code
- **CO2 Emissions (g)**: Carbon footprint based on regional electricity grid
- **CPU Time (ms)**: Processing time estimation
- **Memory Usage (MB)**: Estimated memory footprint
- **Complexity Score**: Code complexity rating

### Real-World Impact

See how your code translates to real-world equivalents:
- **Light Bulb Hours**: How long a 60W bulb could run
- **Tree Planting Days**: Equivalent CO2 offset
- **Car Miles**: Equivalent car emissions

### Optimization Suggestions

Each suggestion includes:
- **Finding**: What was detected
- **Before/After Code**: Code examples showing the improvement
- **Explanation**: Why this helps
- **Predicted Improvement**: Expected score increase
- **Severity**: Low, Medium, or High priority

## Badges and Achievements

### Earning Badges

Badges are automatically awarded when you:
- Submit your first code analysis
- Reach certain green score thresholds
- Maintain submission streaks
- Save specific amounts of CO2
- Complete milestones

### Badge Types

- **First Steps**: Beginner achievements
- **Green Master**: High green scores
- **Consistency**: Streak-related badges
- **Impact**: CO2 and energy savings
- **Expert**: Advanced achievements

### Viewing Your Badges

1. Go to your **Dashboard**
2. Click on **"Badges"** section
3. See earned badges and progress toward new ones

## Teams and Collaboration

### Creating a Team

1. Navigate to **"Teams"**
2. Click **"Create Team"**
3. Enter team name and description
4. Invite members by email

### Team Features

- **Shared Projects**: Collaborate on code analysis
- **Team Leaderboard**: Compare green scores
- **Team Metrics**: Aggregate statistics
- **Project Tracking**: Monitor team progress

### Joining a Team

1. Accept team invitation via email
2. Or search for public teams
3. Request to join

## Dashboard and Metrics

### Personal Dashboard

View your:
- **Average Green Score**: Overall performance
- **Total Submissions**: Number of analyses
- **CO2 Saved**: Total carbon footprint reduction
- **Current Streak**: Consecutive days with submissions
- **Badges Earned**: Achievement count

### Metrics History

- **Timeline View**: See your progress over time
- **Language Breakdown**: Performance by programming language
- **Carbon Timeline**: CO2 savings over time
- **Submission Calendar**: Visual submission history

### Leaderboard

Compete with other users:
- **Weekly**: Top performers this week
- **Monthly**: Top performers this month
- **All Time**: Historical leaders

Filter by timeframe and see rankings, green scores, and badges.

## AI Chatbot

### Asking Questions

1. Click on the **Chatbot** icon
2. Type your question about green coding
3. Get instant answers with examples

### Example Questions

- "How do I optimize loops in Python?"
- "What's the best way to reduce memory usage?"
- "Explain energy-efficient data structures"
- "How to write sustainable JavaScript code?"

### Getting Suggestions

The chatbot provides:
- **Direct Answers**: Clear explanations
- **Code Examples**: Practical implementations
- **Related Topics**: Learn more about the subject
- **Best Practices**: Industry standards

## Tips and Best Practices

### Improving Your Green Score

1. **Use Efficient Algorithms**: Choose O(n log n) over O(n²)
2. **Optimize Loops**: Use list comprehensions, vectorization
3. **Reduce Memory**: Avoid unnecessary copies, use generators
4. **Cache Results**: Store expensive computations
5. **Lazy Evaluation**: Only compute what you need

### Language-Specific Tips

**Python:**
- Use list comprehensions instead of loops
- Leverage built-in functions (map, filter, reduce)
- Use generators for large datasets
- Prefer `collections` module for efficiency

**JavaScript:**
- Use `const` and `let` appropriately
- Avoid global variables
- Use `Array.map()` instead of loops
- Leverage async/await properly

**Java:**
- Use `StringBuilder` for string concatenation
- Prefer `ArrayList` over `LinkedList` for most cases
- Use streams for data processing
- Avoid premature optimization

**C/C++:**
- Use references instead of copies
- Prefer stack allocation when possible
- Avoid memory leaks
- Use const correctness

### Maintaining Your Streak

- Submit code analysis daily
- Even small improvements count
- Use the calendar view to track progress
- Set reminders to maintain consistency

### Maximizing Impact

- Focus on frequently-run code
- Optimize hot paths in applications
- Share knowledge with your team
- Review suggestions regularly

## Troubleshooting

### Code Analysis Fails

- Check that your code is valid syntax
- Ensure the language is correctly selected
- Verify code isn't too large (max 1MB)
- Try breaking large files into smaller chunks

### Can't See Results

- Refresh the page
- Check your internet connection
- Verify you're logged in (for saved analyses)
- Contact support if issues persist

### Badges Not Appearing

- Badges are awarded automatically
- Check your dashboard for updates
- Some badges require specific conditions
- Wait a few minutes after meeting criteria

## Getting Help

- **Documentation**: Check API docs at `/docs`
- **Support**: Contact support@example.com
- **Community**: Join our Discord server
- **FAQ**: Visit the FAQ section

## Privacy and Security

- Your code is analyzed securely
- Code content is encrypted in transit
- Results are stored securely
- You can delete submissions anytime
- See our Privacy Policy for details

---

**Happy Green Coding! 🌱**

