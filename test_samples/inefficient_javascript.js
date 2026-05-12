/**
 * Inefficient JavaScript Code — For Green Coding Advisor Testing
 * Contains anti-patterns that the optimizer should detect.
 */

// 1. Await inside loop (should use Promise.all)
async function fetchUserData(userIds) {
    const results = [];
    for (let i = 0; i < userIds.length; i++) {
        const response = await fetch(`/api/users/${userIds[i]}`);
        const data = await response.json();
        results.push(data);
    }
    return results;
}

// 2. innerHTML += in loop (DOM thrashing)
function renderList(items) {
    const container = document.getElementById('list');
    for (let i = 0; i < items.length; i++) {
        container.innerHTML += `<div class="item">${items[i].name}</div>`;
    }
}

// 3. Index-based iteration instead of for...of
function calculateTotal(prices) {
    let total = 0;
    for (let i = 0; i < prices.length; i++) {
        total += prices[i];
    }
    return total;
}

// 4. String concatenation in loop
function buildReport(data) {
    let report = "";
    for (let i = 0; i < data.length; i++) {
        report += "Item: " + data[i].name + ", Price: $" + data[i].price + "\n";
    }
    return report;
}

// 5. Nested loops for search (should use Set/Map)
function findCommonElements(arr1, arr2) {
    const common = [];
    for (let i = 0; i < arr1.length; i++) {
        for (let j = 0; j < arr2.length; j++) {
            if (arr1[i] === arr2[j]) {
                common.push(arr1[i]);
            }
        }
    }
    return common;
}

// 6. Repeated DOM queries in loop
function updatePrices(newPrices) {
    for (let i = 0; i < newPrices.length; i++) {
        document.getElementById('price-' + i).textContent = newPrices[i];
        document.getElementById('price-' + i).style.color = newPrices[i] > 100 ? 'red' : 'green';
    }
}

// 7. Not using array methods
function getActiveUsers(users) {
    const active = [];
    for (let i = 0; i < users.length; i++) {
        if (users[i].isActive === true) {
            active.push(users[i].name);
        }
    }
    return active;
}

// Test
const prices = [10, 20, 30, 40, 50];
console.log("Total:", calculateTotal(prices));
console.log("Common:", findCommonElements([1, 2, 3, 4], [3, 4, 5, 6]));
console.log("Active:", getActiveUsers([
    { name: "Alice", isActive: true },
    { name: "Bob", isActive: false },
    { name: "Charlie", isActive: true }
]));
