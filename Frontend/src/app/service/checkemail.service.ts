export function checkEmailAddress(emailInput: string): boolean {
  // checking if email address is valid
  var at = false; // email address needs an @
  var dot = false; // email address needs a . after the @
  var chars_after_dot = 0; // top level domain has to be at least 2 chars long
  for (let i = 0; i < emailInput.length; i++) {
    if (at) {
      if ('.'== emailInput.charAt(i)) {
        dot = true;
        chars_after_dot = 0;
      } else {
        chars_after_dot += 1;
      }
      if (!(/[0-9a-zA-Z\.-]/.test(emailInput.charAt(i)))) { // we can only have alphanumeric chars, . and - in the domain part
        return false;
      }
    } else {
      if ('@'== emailInput.charAt(i)) {
        at = true;
      }
    }
  }
  if (!(at && dot && (chars_after_dot > 1))) {
    return false;
  }
  if (/[\W_][\W_]/.test(emailInput)) { // we cant have two special chars in a row
    return false;
  }
  if (/[\W_]/.test(emailInput.charAt(0))) { // we cant start with a special char
    return false;
  }
  return true
}
