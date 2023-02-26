{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, flake-utils, nixpkgs }:
    {
      overlays.default = final: prev: {
        inherit (self.packages.${prev.system}) year-of-bot;
      };

      nixosModules.default = ./nixos-module.nix;
    } // flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in {
        packages.year-of-bot = with pkgs;
          stdenvNoCC.mkDerivation {
            pname = "year-of-bot";
            version = "0.1.0";

            src = ./.;

            buildInputs = [
              (python3.buildEnv.override {
                extraLibs = [ python3Packages.aiohttp python3Packages.yarl ];
              })
            ];

            installPhase = ''
              mkdir -p $out/bin
              cp -r * $out/bin
              chmod +x $out/bin/year-of-bot.py
            '';

            verifyPhase = ''
              $out/bin/year-of-bot.py verify
            '';

            meta = {
              description = "A Pleroma bot that makes technology predictions.";
              mainProgram = "year-of-bot.py";
              license = lib.licenses.agpl3Only;
            };
          };

        packages.default = self.packages.${system}.year-of-bot;

        devShells.default = with pkgs;
          mkShell {
            buildInputs =
              [ python3Packages.aiohttp python3Packages.yarl shellcheck ];
          };
      });
}
