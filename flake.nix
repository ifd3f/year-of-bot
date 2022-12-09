{
  description = "A very basic flake";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }: let pkgs = nixpkgs.legacyPackages.x86_64-linux; in {
    devShells.x86_64-linux.default = with pkgs; mkShell {
      buildInputs = [
        python3Packages.aiohttp
        python3Packages.yarl
      ];
    };
  };
}
