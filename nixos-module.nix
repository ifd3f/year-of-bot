{ pkgs, lib, config, ... }:
let
  cfg = config.services.year-of-bot;
  defaultUser = "yearofbot";
in with lib; {
  options.services.year-of-bot = {
    enable = mkEnableOption "year-of-bot";
    user = mkOption {
      type = types.str;
      description = "User to run under";
      default = defaultUser;
    };
    group = mkOption {
      type = types.str;
      description = "Group to run under";
      default = defaultUser;
    };
    server = mkOption {
      type = types.str;
      description = "Fediverse server to post to";
      example = "https://fedi.astrid.tech";
    };
    postOnCalendar = mkOption {
      type = types.str;
      description = "systemd OnCalendar specification";
      default = "*-*-* *:30:00";
    };
    accessTokenFile = mkOption {
      type = types.path;
      description = ''
        Path to file containing the access token.

        To generate one, see here: https://prplecake.github.io/pleroma-access-token/
      '';
      default = "/var/lib/secrets/year-of-bot/accessToken";
    };
  };

  config = mkIf cfg.enable {
    systemd.services.year-of-bot-config = {
      description = "Set up year-of-bot required directories";
      environment = { inherit (cfg) user group accessTokenFile; };

      script = ''
        mkdir -p "$(dirname "$accessTokenFile")"
        chown -R "$user:$group" "$(dirname "$accessTokenFile")"
      '';
    };

    systemd.services.year-of-bot = {
      description = "Technology Prediction Pleroma Bot";
      wants = [ "year-of-bot-config.service" ];
      path = with pkgs; [ year-of-bot ];
      environment = {
        SERVER_URL = cfg.server;
        ACCESS_TOKEN_PATH = cfg.accessTokenFile;
      };

      script = ''
        export ACCESS_TOKEN="$(cat "$ACCESS_TOKEN_PATH")"
        ${pkgs.year-of-bot}/bin/year-of-bot.py
      '';

      unitConfig = {
        # Access token file must exist to run this service 
        ConditionPathExists = [ cfg.accessTokenFile ];
      };

      serviceConfig = {
        User = cfg.user;
        Group = cfg.group;
      };
    };

    systemd.timers.year-of-bot = {
      wantedBy = [ "network-online.target" ];
      timerConfig.OnCalendar = cfg.postOnCalendar;
    };

    users.users = optionalAttrs (cfg.user == defaultUser) {
      ${defaultUser} = {
        group = cfg.group;
        isSystemUser = true;
      };
    };

    users.groups =
      optionalAttrs (cfg.group == defaultUser) { ${defaultUser} = { }; };
  };
}
