# -*- encoding: utf-8 -*-
# stub: jekyll-gfm-admonitions 1.4.4 ruby lib

Gem::Specification.new do |s|
  s.name = "jekyll-gfm-admonitions".freeze
  s.version = "1.4.4".freeze

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Robin De Schepper".freeze]
  s.date = "2026-07-04"
  s.description = "This plugin allows you to use GitHub-flavored markdown syntaxto create admonition blocks in Jekyll sites.".freeze
  s.email = ["robin.deschepper93@gmail.com".freeze]
  s.homepage = "https://github.com/helveg/jekyll-gfm-admonitions".freeze
  s.licenses = ["MIT".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 2.7.0".freeze)
  s.rubygems_version = "3.5.22".freeze
  s.summary = "A Jekyll plugin to render GitHub-flavored admonitions.".freeze

  s.installed_by_version = "3.6.7".freeze

  s.specification_version = 4

  s.add_runtime_dependency(%q<cssminify>.freeze, ["~> 1.0".freeze])
  s.add_runtime_dependency(%q<jekyll>.freeze, [">= 3.0".freeze, "< 5.0".freeze])
  s.add_runtime_dependency(%q<octicons>.freeze, ["~> 19.8".freeze])
  s.add_development_dependency(%q<bundler>.freeze, ["~> 2.0".freeze])
  s.add_development_dependency(%q<rspec>.freeze, ["~> 3.13".freeze])
  s.add_development_dependency(%q<rake>.freeze, ["~> 13.0".freeze])
end
