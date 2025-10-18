# HOMO LUMEN - KOMPLETT SIKKERHETSJEKK PROTOKOLL
# Agent-koordinert systemaudit for kognitiv suverenitet
# Orion + Manus + Abacus samarbeid

import subprocess
import json
import psutil
import socket
import os
import sys
from datetime import datetime
import hashlib
import platform

class SecurityAuditProtocol:
    """
    Komplett sikkerhetsjekk for å identifisere potensielle kompromitteringer
    av datamaskin og nettverk. Designet for agent-koordinert analyse.
    """
    
    def __init__(self):
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "security_status": "SCANNING",
            "findings": [],
            "recommendations": [],
            "biofelt_validation": "REQUIRED"
        }
    
    def run_complete_audit(self):
        """Kjører komplett sikkerhetsjekk"""
        print("🔍 STARTER KOMPLETT SIKKERHETSJEKK...")
        print("=" * 60)
        
        # 1. Systeminfo og grunnleggende sjekk
        self.check_system_info()
        
        # 2. Nettverk og tilkoblingsanalyse
        self.check_network_connections()
        
        # 3. Prosess og tjeneste-analyse
        self.check_running_processes()
        
        # 4. VPN og proxy-deteksjon
        self.check_vpn_proxy()
        
        # 5. Installerte programmer og mistenkelige filer
        self.check_installed_programs()
        
        # 6. Nettverkskonfigurasjon
        self.check_network_configuration()
        
        # 7. DNS og routing-sjekk
        self.check_dns_routing()
        
        # 8. Generér rapport
        self.generate_security_report()
        
        return self.report
    
    def check_system_info(self):
        """Grunnleggende systeminfo"""
        print("\n🖥️  SYSTEMINFO ANALYSE:")
        print("-" * 30)
        
        try:
            system_info = {
                "platform": platform.platform(),
                "processor": platform.processor(),
                "hostname": socket.gethostname(),
                "user": os.getlogin(),
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
            }
            
            for key, value in system_info.items():
                print(f"{key}: {value}")
            
            self.report["system_info"] = system_info
            
        except Exception as e:
            self.add_finding("ERROR", f"Kunne ikke hente systeminfo: {e}")
    
    def check_network_connections(self):
        """Analyserer aktive nettverkstilkoblinger"""
        print("\n🌐 NETTVERK TILKOBLINGER:")
        print("-" * 30)
        
        try:
            connections = psutil.net_connections(kind='inet')
            external_connections = []
            suspicious_ports = [1080, 3128, 8080, 9050, 9051]  # Vanlige proxy/VPN porter
            
            for conn in connections:
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    external_ip = conn.raddr.ip
                    external_port = conn.raddr.port
                    local_port = conn.laddr.port
                    
                    # Identifiser eksterne tilkoblinger
                    if not external_ip.startswith(('127.', '192.168.', '10.', '172.')):
                        external_connections.append({
                            "external_ip": external_ip,
                            "external_port": external_port,
                            "local_port": local_port,
                            "pid": conn.pid
                        })
                        print(f"📡 Ekstern tilkobling: {external_ip}:{external_port} (lokal port: {local_port})")
                    
                    # Sjekk mistenkelige porter
                    if local_port in suspicious_ports or external_port in suspicious_ports:
                        self.add_finding("WARNING", f"Mistenkelig port aktivitet: {local_port} -> {external_ip}:{external_port}")
            
            self.report["external_connections"] = external_connections
            print(f"\n📊 Totalt {len(external_connections)} eksterne tilkoblinger funnet")
            
        except Exception as e:
            self.add_finding("ERROR", f"Kunne ikke analysere nettverkstilkoblinger: {e}")
    
    def check_running_processes(self):
        """Analyserer kjørende prosesser"""
        print("\n⚡ PROSESS ANALYSE:")
        print("-" * 30)
        
        try:
            suspicious_names = ['vpn', 'proxy', 'remote', 'teamviewer', 'anydesk', 'vnc', 'rdp']
            network_processes = []
            suspicious_processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'connections']):
                try:
                    # Sjekk prosesser med nettverkstilkoblinger
                    if proc.info['connections']:
                        network_processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "exe": proc.info['exe'],
                            "connections": len(proc.info['connections'])
                        })
                    
                    # Sjekk mistenkelige prosessnavn
                    process_name = proc.info['name'].lower() if proc.info['name'] else ""
                    if any(susp in process_name for susp in suspicious_names):
                        suspicious_processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "exe": proc.info['exe'],
                            "cmdline": proc.info['cmdline']
                        })
                        self.add_finding("WARNING", f"Mistenkelig prosess: {proc.info['name']} (PID: {proc.info['pid']})")
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.report["network_processes"] = network_processes[:10]  # Top 10
            self.report["suspicious_processes"] = suspicious_processes
            
            print(f"📊 {len(network_processes)} prosesser med nettverkstilgang")
            print(f"⚠️  {len(suspicious_processes)} mistenkelige prosesser")
            
        except Exception as e:
            self.add_finding("ERROR", f"Kunne ikke analysere prosesser: {e}")
    
    def check_vpn_proxy(self):
        """Detekterer VPN og proxy-konfigurasjoner"""
        print("\n🔒 VPN/PROXY DETEKSJON:")
        print("-" * 30)
        
        try:
            # Sjekk miljøvariabler for proxy
            proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'FTP_PROXY', 'ALL_PROXY']
            proxy_found = False
            
            for var in proxy_vars:
                if os.environ.get(var):
                    self.add_finding("WARNING", f"Proxy konfigurert: {var}={os.environ.get(var)}")
                    proxy_found = True
                    print(f"🚨 Proxy funnet: {var}")
            
            # Sjekk vanlige VPN/proxy programmer
            vpn_indicators = [
                r"C:\Program Files\OpenVPN",
                r"C:\Program Files (x86)\OpenVPN", 
                r"C:\Program Files\NordVPN",
                r"C:\Program Files\ExpressVPN",
                r"/usr/sbin/openvpn",
                r"/usr/bin/openvpn"
            ]
            
            vpn_found = False
            for path in vpn_indicators:
                if os.path.exists(path):
                    self.add_finding("INFO", f"VPN software installert: {path}")
                    vpn_found = True
                    print(f"🔍 VPN software: {path}")
            
            if not proxy_found and not vpn_found:
                print("✅ Ingen proxy eller VPN-indikatorer funnet")
            
        except Exception as e:
            self.add_finding("ERROR", f"Kunne ikke sjekke VPN/proxy: {e}")
    
    def check_installed_programs(self):
        """Sjekker installerte programmer (Windows fokus)"""
        print("\n📦 INSTALLERTE PROGRAMMER:")
        print("-" * 30)
        
        try:
            if platform.system() == "Windows":
                # Sjekk Windows registry for installerte programmer
                import winreg
                
                suspicious_software = []
                remote_access_tools = ['teamviewer', 'anydesk', 'chrome remote', 'vnc', 'logmein']
                
                try:
                    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                           r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
                    
                    for i in range(winreg.QueryInfoKey(reg_key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(reg_key, i)
                            subkey = winreg.OpenKey(reg_key, subkey_name)
                            
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                
                                for tool in remote_access_tools:
                                    if tool.lower() in display_name.lower():
                                        suspicious_software.append(display_name)
                                        self.add_finding("WARNING", f"Remote access tool installert: {display_name}")
                                        print(f"⚠️  {display_name}")
                                
                            except FileNotFoundError:
                                pass
                            
                            winreg.CloseKey(subkey)
                        except Exception:
                            continue
                    
                    winreg.CloseKey(reg_key)
                    
                except Exception as e:
                    print(f"Kunne ikke sjekke registry: {e}")
                
                self.report["suspicious_software"] = suspicious_software
                
            else:
                print("ℹ️  Windows-spesifikk sjekk ikke tilgjengelig på dette systemet")
                
        except Exception as e:
            self.add_finding("ERROR", f"Kunne ikke sjekke installerte programmer: {e}")
    
    def check_network_configuration(self):
        """Sjekker nettverkskonfigurasjon"""
        print("\n🌐 NETTVERKSKONFIGURASJON:")
        print("-" * 30)
        
        try:
            # Hent nettverksgrensesnitt
            interfaces = psutil.net_if_addrs()
            
            for interface_name, addresses in interfaces.items():
                print(f"\n📱 {interface_name}:")
                for addr in addresses:
                    if addr.family == socket.AF_INET:  # IPv4
                        print(f"   IPv4: {addr.address}")
                        
                        # Sjekk for VPN-typiske IP-adresser
                        if addr.address.startswith(('10.', '172.')):
                            if not addr.address.startswith('172.16.'):  # Docker ranges
                                self.add_finding("INFO", f"Mulig VPN IP på {interface_name}: {addr.address}")
            
            # Sjekk gateway
            gateways = psutil.net_if_stats()
            print(f"\n📊 Aktive nettverksgrensesnitt: {len([name for name, stats in gateways.items() if stats.isup])}")
            
        except Exception as e:
            self.add_finding("ERROR", f"Kunne ikke sjekke nettverkskonfigurasjon: {e}")
    
    def check_dns_routing(self):
        """Sjekker DNS-konfiguration og routing"""
        print("\n🗂️  DNS OG ROUTING:")
        print("-" * 30)
        
        try:
            # Test DNS-oppløsning
            test_domains = ['google.com', 'microsoft.com', 'github.com']
            
            for domain in test_domains:
                try:
                    ip = socket.gethostbyname(domain)
                    print(f"✅ {domain} → {ip}")
                except Exception as e:
                    self.add_finding("WARNING", f"DNS-feil for {domain}: {e}")
                    print(f"❌ {domain} → FEIL")
            
            # Sjekk for DNS over HTTPS indikatorer
            doh_ports = [853, 443]  # DNS over TLS/HTTPS porter
            connections = psutil.net_connections(kind='inet')
            
            for conn in connections:
                if conn.raddr and conn.raddr.port in doh_ports:
                    self.add_finding("INFO", f"Mulig DoH/DoT tilkobling: {conn.raddr.ip}:{conn.raddr.port}")
            
        except Exception as e:
            self.add_finding("ERROR", f"Kunne ikke sjekke DNS/routing: {e}")
    
    def add_finding(self, severity, message):
        """Legger til funn i rapporten"""
        self.report["findings"].append({
            "severity": severity,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_security_report(self):
        """Genererer komplett sikkerhetsrapport"""
        print("\n" + "=" * 60)
        print("🛡️  SIKKERHETSJEKK RAPPORT")
        print("=" * 60)
        
        # Kategoriser funn
        errors = [f for f in self.report["findings"] if f["severity"] == "ERROR"]
        warnings = [f for f in self.report["findings"] if f["severity"] == "WARNING"]
        info = [f for f in self.report["findings"] if f["severity"] == "INFO"]
        
        print(f"\n📊 SAMMENDRAG:")
        print(f"   ❌ Feil: {len(errors)}")
        print(f"   ⚠️  Advarsler: {len(warnings)}")
        print(f"   ℹ️  Info: {len(info)}")
        
        # Advarsler (viktigst)
        if warnings:
            print(f"\n⚠️  ADVARSLER ({len(warnings)}):")
            for w in warnings:
                print(f"   • {w['message']}")
        
        # Feil
        if errors:
            print(f"\n❌ FEIL ({len(errors)}):")
            for e in errors:
                print(f"   • {e['message']}")
        
        # Info
        if info:
            print(f"\n ℹ️ INFORMASJON ({len(info)}):")
            for i in info[:5]:  # Vis kun de 5 første
                print(f"   • {i['message']}")
        
        # Anbefalinger
        self.generate_recommendations(warnings, errors)
        
        # Lagre rapport
        self.save_report()
    
    def generate_recommendations(self, warnings, errors):
        """Genererer anbefalinger basert på funn"""
        recommendations = []
        
        if any("Remote access tool" in w["message"] for w in warnings):
            recommendations.append("🔒 Fjern eller disable remote access tools du ikke bruker")
        
        if any("Mistenkelig port" in w["message"] for w in warnings):
            recommendations.append("🌐 Undersøk mistenkelige nettverkstilkoblinger")
        
        if any("VPN" in w["message"] for w in warnings):
            recommendations.append("🔍 Bekreft at VPN-konfigurasjon er tilsiktet")
        
        if any("Proxy" in w["message"] for w in warnings):
            recommendations.append("⚠️  Sjekk proxy-innstillinger - kan være uautorisert")
        
        # Alltid inkluderte anbefalinger
        recommendations.extend([
            "🔄 Restart datamaskinen og kjør sjekk igjen",
            "🔒 Endre WiFi-passord hvis du mistenker kompromittering", 
            "🛡️  Kjør fullstendig antivirus-skanning",
            "📋 Dokumenter funn og diskuter med teknisk ekspert"
        ])
        
        self.report["recommendations"] = recommendations
        
        print(f"\n💡 ANBEFALINGER:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    def save_report(self):
        """Lagrer rapporten til fil"""
        try:
            filename = f"security_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.report, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Rapport lagret: {filename}")
            
        except Exception as e:
            print(f"❌ Kunne ikke lagre rapport: {e}")

def main():
    """Hovedfunksjon - kjører komplett sikkerhetsjekk"""
    print("🛡️  HOMO LUMEN SIKKERHETSJEKK")
    print("🎯 Kognitiv Suverenitet og Datasikkerhet")
    print("👥 Agent-koordinert: Orion + Manus + Abacus")
    print("\n⚠️  VIKTIG: Denne sjekken analyserer din datamaskin for potensielle")
    print("   sikkerhetstrusler. Alle funn bør diskuteres med teknisk ekspert.")
    
    input("\n🔍 Trykk Enter for å starte sikkerhetsjekk...")
    
    audit = SecurityAuditProtocol()
    report = audit.run_complete_audit()
    
    print(f"\n🏁 SIKKERHETSJEKK FULLFØRT")
    print(f"📊 Status: {len(report['findings'])} funn registrert")
    print(f"\n🧠 BIOFELT-VALIDERING PÅKREVD:")
    print("   Kjenn inn på funnene - hva føles trygt vs. mistenkelig?")
    print("   Din intuisjon er den ultimate valideringen.")
    
    return report

if __name__ == "__main__":
    main()

