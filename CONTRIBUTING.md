# Contributing to PentestNetFilter

Thank you for considering contributing to PentestNetFilter! This project aims to provide a lightweight, hackable network filter for penetration testing and security research.

## 🎯 Project Goals

- **Lightweight**: Minimal resource usage, non-intrusive operation
- **Pentest-friendly**: Designed for security professionals and researchers  
- **Hackable**: Easy to modify and extend for specific use cases
- **Educational**: Help users understand network behavior

## 🤝 How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or request features
- Include your OS, Python version, and steps to reproduce
- For security issues, please contact maintainers privately first

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly (especially with different OS configurations)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Documentation
- Improve README, guides, or code comments
- Add new rule configurations for specific use cases
- Create tutorials or walkthroughs

## 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/pentest-netfilter
cd pentest-netfilter

# Install development dependencies
pip3 install psutil scapy

# Test the application
python3 demo.py --demo
sudo python3 netfilter.py --help
```

## 📝 Coding Guidelines

### Python Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and modular

### Rule Configurations
- Use clear, descriptive rule descriptions
- Categorize rules appropriately (essential, pentest, privacy, etc.)
- Test rules thoroughly before submitting

### Documentation
- Update README.md for new features
- Add examples for new functionality
- Keep documentation clear and beginner-friendly

## 🧪 Testing

Before submitting changes:

```bash
# Test basic functionality
python3 demo.py --demo

# Test rule loading
python3 -c "
import json
with open('default_rules.json') as f:
    rules = json.load(f)
    print(f'Loaded {len(rules[\"rules\"])} rules successfully')
"

# Test in VM (if available)
sudo python3 netfilter.py --config example_rules.json --help
```

## 🎨 Ideas for Contributions

### New Features
- GUI interface using tkinter or web-based dashboard
- Integration with other security tools
- Advanced logging and reporting
- Custom rule creation wizard
- Performance optimizations

### Rule Sets
- CTF-specific rule configurations
- Malware analysis rule sets  
- Privacy-focused configurations
- Enterprise pentest rule templates

### Platform Support
- Improved container support
- Better VMware/VirtualBox integration
- Cloud deployment guides
- Raspberry Pi optimization

### Documentation
- Video tutorials
- Advanced use case guides
- Integration with popular pentest frameworks
- Troubleshooting guides

## ⚖️ Code of Conduct

### Our Standards
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication

### Unacceptable Behavior
- Harassment or discrimination
- Sharing this tool for malicious purposes
- Unauthorized testing on systems you don't own
- Violating applicable laws or regulations

## 🚨 Security and Responsible Use

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ Security research and education  
- ✅ Privacy protection on your own systems
- ✅ Learning network behavior

NOT for:
- ❌ Unauthorized access or testing
- ❌ Malicious activities
- ❌ Violating terms of service
- ❌ Any illegal activities

## 📞 Contact

- GitHub Issues: For bugs and feature requests
- Discussions: For questions and community interaction
- Security Issues: Contact maintainers privately

---

**Remember**: This project exists to improve security education and authorized testing. Please use responsibly! 🔥
