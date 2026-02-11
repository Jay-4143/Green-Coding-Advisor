
// Inefficient JavaScript Code Patterns
// This file is designed to trigger Green Coding Advisor warnings

async function inefficientJavaScript() {
    console.log("Running inefficient JS code...");
    const start = Date.now();

    // 1. Traditional for-loop with index access (Pattern: traditional for)
    // Metric: Less efficient than for...of or optimized array methods
    const items = new Array(50000).fill(0).map((_, i) => i);
    const result = [];

    console.log("1. Testing loop inefficiency...");
    for (let i = 0; i < items.length; i++) {
        // Inefficient: accessing by index
        const item = items[i];
        // Inefficient: pushing one by one in loop
        if (item % 2 === 0) {
            result.push(item * 2);
        }
    }

    // 2. String concatenation (Pattern: += string)
    // Metric: Creates many intermediate string objects
    console.log("2. Testing string inefficiency...");
    let longString = "";
    for (let i = 0; i < 5000; i++) {
        longString += "item_" + i + ", ";
    }

    // 3. Sequential await in loop (Pattern: await in loop)
    // Metric: Blocks execution, prevents parallelization
    console.log("3. Testing async inefficiency...");
    const urls = ["url1", "url2", "url3", "url4", "url5"];

    const mockFetch = (url) => new Promise(resolve => setTimeout(() => resolve(url), 10));

    for (let i = 0; i < urls.length; i++) {
        // Inefficient: await inside loop makes requests sequential
        // Should use Promise.all()
        await mockFetch(urls[i]);
    }

    // 4. Repeated DOM access (Simulated)
    // Metric: DOM access is slow
    console.log("4. Testing DOM inefficiency (simulated)...");
    const container = { innerHTML: "" }; // Mock DOM element
    for (let i = 0; i < 1000; i++) {
        // Inefficient: modifying layout repeatedly
        container.innerHTML += `<div>Item ${i}</div>`;
    }

    const end = Date.now();
    console.log(`Inefficient JS finished in ${end - start}ms`);
}

inefficientJavaScript();
