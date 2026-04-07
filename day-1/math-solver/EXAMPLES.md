# Examples and Use Cases

Real examples of math problems that work well with the Math Solver.

## Quick Examples to Try

Try these in the frontend:

### Arithmetic

```
What is 25% of 80?
```

**Expected Output:**
```
Step 1: Convert 25% to decimal form: 25% = 0.25
Step 2: Multiply 80 by 0.25: 80 × 0.25 = 20
Answer: 25% of 80 is 20
```

---

```
Calculate 15 × 12
```

**Expected Output:**
```
Step 1: Break down 15 × 12 as (10 + 5) × 12
Step 2: 10 × 12 = 120
Step 3: 5 × 12 = 60  
Step 4: 120 + 60 = 180
Answer: 15 × 12 = 180
```

---

### Basic Algebra

```
Solve: 2x + 5 = 15
```

**Expected Output:**
```
Step 1: We have the equation: 2x + 5 = 15
Step 2: Subtract 5 from both sides: 2x = 15 - 5 = 10
Step 3: Divide both sides by 2: x = 10 ÷ 2 = 5
Step 4: Check: 2(5) + 5 = 10 + 5 = 15 ✓
Answer: x = 5
```

---

```
Find x: 3(x - 2) = 18
```

**Expected Output:**
```
Step 1: Expand the left side: 3x - 6 = 18
Step 2: Add 6 to both sides: 3x = 24
Step 3: Divide by 3: x = 8
Answer: x = 8
```

---

### Geometry

```
A circle has radius 5 cm. What is its area?
```

**Expected Output:**
```
Step 1: The formula for area of a circle is A = πr²
Step 2: Given: r = 5 cm
Step 3: A = π × 5² = π × 25 = 25π cm²
Step 4: In decimal: 25π ≈ 78.54 cm²
Answer: The area is 25π cm² or approximately 78.54 cm²
```

---

### Word Problems

```
If a book costs $15 and is on sale for 20% off, how much will you pay?
```

**Expected Output:**
```
Step 1: Find the discount amount: 20% of $15
Step 2: Discount = 0.20 × $15 = $3
Step 3: Sale price = Original price - Discount
Step 4: Sale price = $15 - $3 = $12
Answer: You will pay $12
```

---

```
A train travels 60 mph for 2.5 hours. How far does it go?
```

**Expected Output:**
```
Step 1: Use the formula: Distance = Speed × Time
Step 2: Speed = 60 mph
Step 3: Time = 2.5 hours
Step 4: Distance = 60 × 2.5 = 150 miles
Answer: The train travels 150 miles
```

---

### Fractions

```
Simplify: 18/24
```

**Expected Output:**
```
Step 1: Find the GCD of 18 and 24: GCD = 6
Step 2: Divide numerator by GCD: 18 ÷ 6 = 3
Step 3: Divide denominator by GCD: 24 ÷ 6 = 4
Answer: 18/24 simplified is 3/4
```

---

```
Calculate: 2/3 + 3/4
```

**Expected Output:**
```
Step 1: Find common denominator: LCD of 3 and 4 is 12
Step 2: Convert 2/3 = 8/12
Step 3: Convert 3/4 = 9/12
Step 4: Add: 8/12 + 9/12 = 17/12 = 1 5/12
Answer: 2/3 + 3/4 = 17/12 or 1 5/12
```

---

### Statistics

```
Find the average of: 10, 15, 20, 25, 30
```

**Expected Output:**
```
Step 1: Add all numbers: 10 + 15 + 20 + 25 + 30 = 100
Step 2: Count the numbers: 5 numbers
Step 3: Divide sum by count: 100 ÷ 5 = 20
Answer: The average is 20
```

---

### Order of Operations (PEMDAS)

```
Solve: 5 + 3 × 2 - 4
```

**Expected Output:**
```
Step 1: Follow PEMDAS (Parentheses, Exponents, Multiplication/Division, Addition/Subtraction)
Step 2: First, do multiplication: 3 × 2 = 6
Step 3: Now we have: 5 + 6 - 4
Step 4: Do addition and subtraction left to right: 5 + 6 = 11
Step 5: Then: 11 - 4 = 7
Answer: 7
```

---

### Exponents

```
Calculate: 2^5
```

**Expected Output:**
```
Step 1: 2^5 means 2 × 2 × 2 × 2 × 2
Step 2: 2 × 2 = 4
Step 3: 4 × 2 = 8
Step 4: 8 × 2 = 16
Step 5: 16 × 2 = 32
Answer: 2^5 = 32
```

---

### Square Roots

```
What is √144?
```

**Expected Output:**
```
Step 1: We need to find the number that, when multiplied by itself, equals 144
Step 2: 12 × 12 = 144
Answer: √144 = 12
```

---

### Quadratic Equations

```
Solve: x² - 5x + 6 = 0
```

**Expected Output:**
```
Step 1: Factor the quadratic: x² - 5x + 6 = (x - 2)(x - 3) = 0
Step 2: Each factor could be zero:
   - If x - 2 = 0, then x = 2
   - If x - 3 = 0, then x = 3
Step 3: Check x = 2: 2² - 5(2) + 6 = 4 - 10 + 6 = 0 ✓
Step 4: Check x = 3: 3² - 5(3) + 6 = 9 - 15 + 6 = 0 ✓
Answer: x = 2 or x = 3
```

## What Works Well

✓ Single-variable algebra
✓ Arithmetic and percentages
✓ Geometry formulas
✓ Word problems
✓ Fractions and decimals
✓ Exponents and roots
✓ Order of operations
✓ Basic statistics
✓ Simple systems of equations
✓ Logic puzzles involving numbers

## What Has Limitations

⚠ Very complex systems of equations (3+ variables)
⚠ Advanced calculus (derivatives, integrals)
⚠ Multi-step optimization problems
⚠ Problems requiring specialized mathematical software
⚠ Highly abstract theoretical proofs

For these, Claude can still help but may need different prompting.

## Customizing the Prompt

To get different behavior, edit the `systemPrompt` in `server.ts`:

### For Verification Only

```typescript
const systemPrompt = `You are a math checker. When given a solution, evaluate if it is correct. 
State clearly: CORRECT or INCORRECT and why.`;
```

Request: `"Check if: 2x + 3 = 7 has solution x = 2"`

### For Quick Answers

```typescript
const systemPrompt = `Provide the most concise solution possible. 
Single number or expression only, no explanation.`;
```

### For Teaching Mode

```typescript
const systemPrompt = `You are a patient math tutor explaining concepts to a high school student. 
Explain WHY each step works, not just HOW.`;
```

### For Contest Math

```typescript
const systemPrompt = `You are solving competition math problems. 
Find elegant, efficient solutions. Show clever techniques.`;
```

## API Response Examples

### Simple Problem

**Request:**
```json
{"problem": "What is 10 + 5?"}
```

**Response:**
```json
{
  "problem": "What is 10 + 5?",
  "solution": "This is a basic addition problem.\nStep 1: We have 10 + 5\nStep 2: Adding these two positive numbers: 10 + 5 = 15\nAnswer: 15",
  "model": "claude-haiku-4-5-20251001",
  "usage": {
    "input_tokens": 47,
    "output_tokens": 68
  }
}
```

### Complex Problem

**Request:**
```json
{"problem": "A store buys widgets for $5 each and sells them for $12 each. If they sell 100 widgets, what is their total profit?"}
```

**Response:**
```json
{
  "problem": "A store buys widgets for $5 each and sells them for $12 each. If they sell 100 widgets, what is their total profit?",
  "solution": "Step 1: Find profit per widget\nProfit per widget = Selling price - Cost price\nProfit per widget = $12 - $5 = $7\n\nStep 2: Find total profit\nTotal profit = Profit per widget × Number of widgets\nTotal profit = $7 × 100 = $700\n\nAnswer: The total profit is $700",
  "model": "claude-haiku-4-5-20251001",
  "usage": {
    "input_tokens": 85,
    "output_tokens": 124
  }
}
```

## Interactive Usage Tips

### For Students

- Try different phrasings of the same problem
- Use it to check homework
- Study how solutions are structured
- Modify numbers and see how answers change

### For Teachers

- Generate custom word problems
- Check student solution approaches
- Create step-by-step answer keys
- Demonstrate alternative solution methods

### For Self-Learning

- Work through problems first, then check
- Read the steps to learn technique
- Ask follow-up questions
- Try harder versions of worked problems

## Batch Testing

Test multiple problems programmatically:

```javascript
const problems = [
  "What is 5 + 3?",
  "Solve: 2x = 10",
  "What is 20% of 50?",
  "Calculate: √25"
];

for (const problem of problems) {
  const result = await fetch('http://localhost:3001/solve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ problem })
  });
  const data = await result.json();
  console.log(`Q: ${data.problem}`);
  console.log(`A: ${data.solution}\n`);
}
```

## Extending with New Problem Types

The system is flexible. Modify `server.ts` to handle:

- Multi-part problems
- Problems with diagrams (text descriptions)
- Check-your-work mode
- Difficulty levels
- Language translation

All by adjusting the prompt and API call.
