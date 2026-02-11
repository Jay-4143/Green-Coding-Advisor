
// Inefficient JavaScript Code Pattern
function inefficientJS() {
    console.log("Running inefficient JS...");
    const start = Date.now();

    const items = Array.from({ length: 100000 }, (_, i) => i);
    const result = [];

    // 1. Traditional for loop with index
    for (let i = 0; i < items.length; i++) {
        result.push(items[i] * 2);
    }

    // 2. String concatenation in loop
    let s = "";
    for (let i = 0; i < 1000; i++) {
        s += i;
    }

    // 3. Sequential await in loop (simulated)
    // async function would be here

    const end = Date.now();
    console.log(`Inefficient JS took: ${end - start}ms`);
}

// Efficient JavaScript Code Pattern
function efficientJS() {
    console.log("Running efficient JS...");
    const start = Date.now();

    const items = Array.from({ length: 100000 }, (_, i) => i);

    // 1. Array methods (map/filter/reduce)
    const result = items.map(x => x * 2);

    // 2. Array join for string building
    const s = Array.from({ length: 1000 }, (_, i) => i).join("");

    // 3. Promise.all for parallel async
    // await Promise.all(promises);

    const end = Date.now();
    console.log(`Efficient JS took: ${end - start}ms`);
}

inefficientJS();
efficientJS();
