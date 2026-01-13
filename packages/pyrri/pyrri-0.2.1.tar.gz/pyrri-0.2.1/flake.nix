{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs = { self, nixpkgs, ... }: {
    packages.x86_64-linux = let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
    in {
      pyrri = pkgs.python3Packages.buildPythonPackage rec {
        pname = "pyrri";
        version = "0.2.1";

        src = ./.;

        format = "pyproject";

        buildInputs = [ pkgs.python3Packages.hatchling ];

        pythonImportsCheck = [ "rri" ];

        meta.mainProgram = "rri";
      };

      docs = pkgs.stdenv.mkDerivation {
        pname = "pyrri-docs";
        version = self.packages.x86_64-linux.pyrri.version;

        src = ./.;

        buildInputs = [
          pkgs.python3.pkgs.mkdocs-material
          pkgs.python3.pkgs.mkdocstrings-python
        ];

        buildPhase = ''
          cp README.md docs/index.md
          python3 -m mkdocs build
        '';

        installPhase = ''
          mkdir -p $out
          cp -r ./site/* $out/
        '';
      };

      default = self.packages.x86_64-linux.pyrri;
    };

    devShells.x86_64-linux = let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
    in {
      pyrri = pkgs.mkShell {
        packages = with pkgs; [ hatch ];
        inputsFrom = [
          self.packages.x86_64-linux.pyrri
          self.packages.x86_64-linux.docs
        ];
      };
      default = self.devShells.x86_64-linux.pyrri;
    };

    hydraJobs = {
      inherit (self)
        packages;
    };
  };
}
