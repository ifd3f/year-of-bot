{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, flake-utils, nixpkgs }:
    {
      overlays.default = final: prev: {
        inherit (self.packages.${prev.system}) year-of-bot;
      };

      nixosModules.default = ./nixos-module.nix;
    } // flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        poetryOverrides = with pkgs;
          poetry2nix.overrides.withDefaults (final: prev: {
            pleroma-py = prev.pleroma-py.overrideAttrs
              (oldAttrs: { buildInputs = [ prev.setuptools ]; });
          });

      in {
        packages.year-of-bot = with pkgs;
          poetry2nix.mkPoetryApplication {
            projectDir = ./.;
            overrides = poetryOverrides;

            doCheck = true;
            checkPhase = ''
              runHook preCheck

              python -m unittest -v tests/**/*.py

              runHook postCheck
            '';

            meta = {
              description = "A Pleroma bot that makes technology predictions.";
              license = lib.licenses.agpl3Only;
            };
          };

        packages.default = self.packages.${system}.year-of-bot;

        devShells.default = with pkgs;
          let
            poetryEnv = poetry2nix.mkPoetryEnv {
              projectDir = ./.;
              overrides = poetryOverrides;
            };
          in mkShell {
            propagatedBuildInputs = [ poetryEnv ];
            buildInputs = [ poetry shellcheck python3Packages.black ];
          };
      });
}
