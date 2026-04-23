import java.util.Scanner;

public class PasswordValidator {

    static boolean hasMinLength(String password) {
        return password.length() >= 8;
    }

    static boolean hasUppercase(String password) {
        for (int i = 0; i < password.length(); i++) {
            if (Character.isUpperCase(password.charAt(i))) {
                return true;
            }
        }
        return false;
    }

    static boolean hasDigit(String password) {
        for (int i = 0; i < password.length(); i++) {
            if (Character.isDigit(password.charAt(i))) {
                return true;
            }
        }
        return false;
    }

    static boolean hasSpecialChar(String password) {
        String special = "!@#$%^&*()_+-=[]{}|;':\",./<>?";
        for (int i = 0; i < password.length(); i++) {
            if (special.indexOf(password.charAt(i)) >= 0) {
                return true;
            }
        }
        return false;
    }

    static String checkStrength(String password) {
        int score = 0;
        if (hasMinLength(password)) score++;
        if (hasUppercase(password)) score++;
        if (hasDigit(password)) score++;
        if (hasSpecialChar(password)) score++;
        if (password.length() >= 12) score++;

        if (score <= 2) return "Weak";
        if (score == 3) return "Moderate";
        if (score == 4) return "Strong";
        return "Very Strong";
    }

    static void printFeedback(String password) {
        System.out.println("\nChecking your password...");
        System.out.println("----------------------------------");

        boolean allPassed = true;

        if (!hasMinLength(password)) {
            System.out.println("  Too short. Must be at least 8 characters.");
            allPassed = false;
        } else {
            System.out.println("  Length is good (" + password.length() + " characters).");
        }

        if (!hasUppercase(password)) {
            System.out.println("  Missing an uppercase letter.");
            allPassed = false;
        } else {
            System.out.println("  Contains an uppercase letter.");
        }

        if (!hasDigit(password)) {
            System.out.println("  Missing a digit.");
            allPassed = false;
        } else {
            System.out.println("  Contains a digit.");
        }

        if (!hasSpecialChar(password)) {
            System.out.println("  Missing a special character (e.g. @, #, !).");
            allPassed = false;
        } else {
            System.out.println("  Contains a special character.");
        }

        System.out.println("----------------------------------");

        if (allPassed) {
            System.out.println("  Password strength : " + checkStrength(password));
            System.out.println("  Your password meets all requirements.");
        }
    }

    static boolean isValid(String password) {
        return hasMinLength(password) && hasUppercase(password) && hasDigit(password) && hasSpecialChar(password);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("------------------------------------------");
        System.out.println("       SafeLog Password Validator         ");
        System.out.println("------------------------------------------");
        System.out.println("Your password must have:");
        System.out.println("  - At least 8 characters");
        System.out.println("  - At least one uppercase letter");
        System.out.println("  - At least one digit");
        System.out.println("  - At least one special character");
        System.out.println("------------------------------------------");

        String password = "";
        int attempts = 0;

        while (!isValid(password)) {
            attempts++;
            System.out.print("\nEnter a password (attempt " + attempts + "): ");
            password = scanner.nextLine();

            printFeedback(password);

            if (!isValid(password)) {
                System.out.println("\nThat password does not meet the requirements. Please try again.");
            }
        }

        System.out.println("\nPassword accepted after " + attempts + " attempt(s).");
        System.out.println("You are good to go.");
        scanner.close();
    }
}