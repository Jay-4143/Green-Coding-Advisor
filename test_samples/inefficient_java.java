import java.util.ArrayList;
import java.util.List;

/**
 * Inefficient Java Code — For Green Coding Advisor Testing
 * Contains anti-patterns that the optimizer should detect.
 */
public class InefficientJava {

    // 1. String concatenation with += in loop (should use StringBuilder)
    public static String buildCsv(List<String[]> rows) {
        String result = "";
        for (int i = 0; i < rows.size(); i++) {
            String[] row = rows.get(i);
            for (int j = 0; j < row.length; j++) {
                result += row[j];
                if (j < row.length - 1) {
                    result += ",";
                }
            }
            result += "\n";
        }
        return result;
    }

    // 2. Using new Integer() instead of autoboxing (deprecated)
    public static List<Integer> convertToIntegers(String[] numbers) {
        List<Integer> result = new ArrayList<>();
        for (int i = 0; i < numbers.length; i++) {
            result.add(new Integer(Integer.parseInt(numbers[i])));
        }
        return result;
    }

    // 3. Index-based loop instead of enhanced for
    public static int calculateSum(List<Integer> numbers) {
        int total = 0;
        for (int i = 0; i < numbers.size(); i++) {
            total += numbers.get(i);
        }
        return total;
    }

    // 4. Nested loops for duplicate detection O(n²)
    public static List<String> findDuplicates(List<String> items) {
        List<String> duplicates = new ArrayList<>();
        for (int i = 0; i < items.size(); i++) {
            for (int j = i + 1; j < items.size(); j++) {
                if (items.get(i).equals(items.get(j))) {
                    if (!duplicates.contains(items.get(i))) {
                        duplicates.add(items.get(i));
                    }
                }
            }
        }
        return duplicates;
    }

    // 5. Manual string reversal instead of StringBuilder.reverse()
    public static String reverseString(String input) {
        String reversed = "";
        for (int i = input.length() - 1; i >= 0; i--) {
            reversed += input.charAt(i);
        }
        return reversed;
    }

    // 6. Not using Collections utility methods
    public static int findMax(List<Integer> numbers) {
        int max = numbers.get(0);
        for (int i = 1; i < numbers.size(); i++) {
            if (numbers.get(i) > max) {
                max = numbers.get(i);
            }
        }
        return max;
    }

    public static void main(String[] args) {
        List<String[]> rows = new ArrayList<>();
        rows.add(new String[]{"Name", "Age", "City"});
        rows.add(new String[]{"Alice", "30", "NYC"});
        rows.add(new String[]{"Bob", "25", "LA"});
        System.out.println("CSV:\n" + buildCsv(rows));

        List<Integer> numbers = new ArrayList<>();
        numbers.add(10); numbers.add(20); numbers.add(30);
        System.out.println("Sum: " + calculateSum(numbers));
        System.out.println("Max: " + findMax(numbers));
        System.out.println("Reversed: " + reverseString("Hello World"));

        List<String> items = new ArrayList<>();
        items.add("apple"); items.add("banana"); items.add("apple"); items.add("cherry");
        System.out.println("Duplicates: " + findDuplicates(items));
    }
}
