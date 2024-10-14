class Aitronos < Formula
  desc "Aitronos CLI for streamlining project setup"
  homepage "https://github.com/yourusername/aitronos-cli"  # Replace with your repo URL
  url "https://github.com/yourusername/aitronos-cli/archive/v1.0.0.tar.gz"  # Replace with your release URL
  sha256 "SHA256_HASH_OF_YOUR_TARBALL"  # Replace with the SHA256 hash
  license "MIT"

  depends_on "python@3.9"  # Specify the Python version you're using

  def install
    system "pip3", "install", "."  # Install your Python package
  end

  test do
    system "#{bin}/aitronos", "--version"  # Replace with a simple command to test the installation
  end
end