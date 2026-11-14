# Package research

What each Amazon package does, what you lose without it, and what dumbtv does with it.
One table, so the lists in `data/` can keep one-line comments and point here.

The "What it does", "Without it" and "Verdict" columns come from
[debloatfiretv](https://github.com/jannikloehr/debloatfiretv) by Jannik Löhr
(`research/packages.md`, MIT, see [CREDITS.md](../CREDITS.md)). It tested every package
on a Fire TV 2-Series television (`AFTKAUK002`, MediaTek, Fire OS 7.7.1.7, PS7717/5741):
a package is `safe` only after it was disabled there and the home screen, Settings and
common apps (Netflix, YouTube, TiviMate) still worked.

The "dumbtv" column is what this repository does with the package on Fire OS 7 and 8
(`data/fireos/`), and `tests/test_packages_doc.py` keeps it in step with the lists:

| dumbtv | Meaning |
|---|---|
| `disabled` | in `packages.txt`: `debloat.sh` disables it on every pass |
| `ALEXA=0` | in `alexa.txt`: disabled only when the owner turns Alexa off |
| `if named` | in `user-apps.txt`: something a person may use; removed only when named |
| `protected` | in `protected.txt`: Amazon refuses `pm disable-user`; `lockdown.sh` starves it and the DNS filter blocks its uploads |
| `never` | in `never-disable.txt`: never touched, even if named |
| — | on no list: dumbtv leaves it alone |

Verdicts from debloatfiretv: `safe` (disabled and checked on a real device), `keep`
(breaks something essential, or kept on purpose), `protected` (Fire OS refuses to
disable it without root). A package that is `safe` there and on no list here has not
been through dumbtv's own checks on a range of TVs; see "A TV the lists do not cover"
in [AGENTS.md](../AGENTS.md) before adding one.

| Package | What it does | Without it | Verdict | dumbtv |
|---|---|---|---|---|
| `com.amazon.tv.acr` | Automatic Content Recognition: fingerprints what is on screen (incl. HDMI/tuner) for ad targeting | None noticed | safe | disabled |
| `com.amazon.tv.fw.metrics` | Fire TV framework metrics | None noticed | safe | disabled |
| `com.amazon.wirelessmetrics.service` | Wi-Fi/BT metrics upload | None noticed | safe | disabled |
| `com.amazon.perfcollection` | Performance data collection | None noticed | safe | disabled |
| `com.amazon.dp.logger` | Device-platform logging | None noticed | safe | disabled |
| `com.amazon.logan` | Log upload agent | None noticed | safe | disabled |
| `com.amazon.neo.minerva.logcat` | Logcat collection for Minerva telemetry | None noticed | safe | disabled |
| `com.amazon.connectivitydiag` | Network diagnostics | None noticed | safe | disabled |
| `com.amazon.hybridadidservice` | Advertising ID service | Apps get no Amazon ad ID | safe | disabled |
| `com.amazon.kso.blackbird` | "Special Offers" ads | Fewer ads | safe | — |
| `com.amazon.sneakpeek` | Auto-playing trailer previews on the home screen | No autoplay previews | safe | disabled |
| `com.amazon.shoptv.client` | Shopping overlays | None noticed | safe | disabled |
| `com.amazon.tv.ftvambient` | Ambient Experience (art/widgets when idle) | No ambient mode | safe | — |
| `com.amazon.bueller.photos` | Amazon Photos app/screensaver source | No Amazon Photos | safe | if named |
| `com.amazon.bueller.music` | Amazon Music integration | No Amazon Music | safe | if named |
| `com.amazon.gamehub` | Luna/games hub | No games row | safe | if named |
| `com.amazon.recess` | Casual games hub | No games | safe | — |
| `com.amazon.minitv.android.app` | Amazon miniTV (India) | None | safe | if named |
| `com.amazon.naatyam` | India content stub | None | safe | — |
| `com.amazon.tahoe` | Amazon Kids (FreeTime) | No Kids profiles | safe | if named |
| `com.amazon.hedwig` | Amazon News | No News app | safe | disabled |
| `com.amazon.cloud9` | Silk browser | No browser | safe | if named |
| `com.amazon.tv.easyupgrade` | Upsell prompts | None | safe | disabled |
| `com.amazon.tv.democontent.provider` | Store-demo content | None | safe | disabled |
| `com.amazon.storm.lightning.tutorial` | Onboarding tutorial | None | safe | never |
| `com.amazon.tmm.tutorial` | Onboarding tutorial | None | safe | disabled |
| `com.amazon.tv.releasenotes` | "What's new" after updates | None | safe | disabled |
| `com.android.printspooler` | Printing | None on a TV | safe | if named |
| `com.android.bips` | Printing | None on a TV | safe | if named |
| `com.amazon.vizzini` | Alexa voice UI | Voice button on the remote does nothing | safe | never |
| `com.amazon.tv.alexaalerts` | Alexa alarms/timers on TV | No alarms on TV | safe | ALEXA=0 |
| `com.amazon.tv.alexanotifications` | Alexa notification banners | No Alexa banners | safe | ALEXA=0 |
| `com.amazon.firetv.androidskillconnectioncapability` | Alexa skills controlling apps | "Alexa, play X in app Y" stops working | safe | ALEXA=0 |
| `com.amazon.alexa.externalmediaplayer.fireos` | Alexa music/media playback | No Alexa music on TV | safe | ALEXA=0 |
| `com.amazon.alexamediaplayer.runtime.ftv` | Alexa music/media playback | No Alexa music on TV | safe | ALEXA=0 |
| `com.amazon.rtcsessioncontroller` | Alexa calling/video calls | No calls | safe | ALEXA=0 |
| `com.amazon.tv.channelscan` | Tuner channel scan | No channel search | safe | never |
| `com.vewd.core.*` | HbbTV/Freeview Play (red button) | No HbbTV | safe | never: com.vewd.core.fvpplayer, com.vewd.core.opapp, com.vewd.core.service, com.vewd.core.tis, com.vewd.core.tvapp |
| `com.amazon.device.metrics` | Device metrics upload | Cannot be disabled (Fire OS refuses) | protected | protected |
| `com.amazon.device.crashmanager` | Crash report upload | Cannot be disabled (Fire OS refuses) | protected | protected |
| `com.amazon.device.logmanager` | Log manager | Cannot be disabled (Fire OS refuses) | protected | — |
| `com.amazon.adep` | Analytics/data event pipeline | Cannot be disabled (Fire OS refuses) | protected | — |
| `com.amazon.tv.csapp` | Customer-service data collection | Cannot be disabled (Fire OS refuses) | protected | protected |
| `com.fireos.usagestats.proxy` | App usage stats | Cannot be disabled (Fire OS refuses) | protected | — |
| `com.amazon.ftvads.deeplinking` | Deep links from home-screen ads | Cannot be disabled (Fire OS refuses) | protected | protected |
| `com.amazon.tv.launcher` | Home screen (also hosts Settings). Do not disable without a replacement launcher | — | keep | never |
| `com.amazon.firehomestarter` | Home screen (also hosts Settings). Do not disable without a replacement launcher | — | keep | never |
| `com.amazon.tv.livetv` | HDMI inputs and the live TV framework (also used by IPTV apps' channel integration) | — | keep | never |
| `com.amazon.mediatek.livetv` | HDMI inputs and the live TV framework (also used by IPTV apps' channel integration) | — | keep | never |
| `com.mediatek.tv*` | HDMI inputs and the live TV framework (also used by IPTV apps' channel integration) | — | keep | — |
| `com.amazon.franktvinput` | HDMI inputs and the live TV framework (also used by IPTV apps' channel integration) | — | keep | never |
| `com.amazon.tifobserver` | HDMI inputs and the live TV framework (also used by IPTV apps' channel integration) | — | keep | never |
| `com.amazon.venezia` | Appstore. Without it, apps no longer update | — | keep | never |
| `com.amazon.dcp` | Account/login, needed by Prime Video etc. | — | keep | — |
| `com.amazon.identity.*` | Account/login, needed by Prime Video etc. | — | keep | — |
| `com.amazon.tcomm*` | Account/login, needed by Prime Video etc. | — | keep | — |
| `com.amazon.imp` | Account/login, needed by Prime Video etc. | — | keep | — |
| `com.amazon.tv.settings*` | Settings, keyboard | — | keep | never: com.amazon.tv.settings.amlogic, com.amazon.tv.settings.core, com.amazon.tv.settings.mediatek, com.amazon.tv.settings.v2 |
| `com.amazon.tv.ime` | Settings, keyboard | — | keep | — |
| `com.amazon.tv.quicksettings*` | Settings, keyboard | — | keep | — |
| `com.amazon.device.software.ota*` | System updates. Disabling blocks security fixes | — | keep | protected: com.amazon.device.software.ota, com.amazon.device.software.ota.override |
| `com.amazon.tv.forcedotaupdater.v2` | System updates. Disabling blocks security fixes | — | keep | disabled |
| `com.amazon.webview.chromium` | WebView used by many apps | — | keep | never |
| `com.amazon.ftv.screensaver` | Screensaver. On TVs it protects the panel from burn-in | — | keep | if named |
| `com.apple.airplay.amazon.airplay` | AirPlay, casting, DIAL (YouTube/Netflix "cast to TV") | — | keep | — |
| `com.amazon.cast.sink` | AirPlay, casting, DIAL (YouTube/Netflix "cast to TV") | — | keep | — |
| `com.amazon.dialservice` | AirPlay, casting, DIAL (YouTube/Netflix "cast to TV") | — | keep | — |
| `com.amazon.whisperlink.*` | Device discovery for the Fire TV phone remote app and Fling | — | keep | — |
| `com.amazon.whisperplay.*` | Device discovery for the Fire TV phone remote app and Fling | — | keep | never: com.amazon.whisperplay.service.install |
| `com.amazon.tv.matter` | Matter smart-home controller | — | keep | — |
| `com.amazon.tv.mattercohost` | Matter smart-home controller | — | keep | — |
| `com.amazon.alexadirectivebrokerservice` | Alexa backend, used by Matter | — | keep | ALEXA=0 |
| `com.amazon.alexa.datastore.app` | Alexa backend, used by Matter | — | keep | ALEXA=0 |
| `amazon.speech.davs.davcservice` | Alexa backend, used by Matter | — | keep | — |
| `com.android.documentsui` | File picker (e.g. restoring app backups) | — | keep | — |
| `com.amazon.device.messaging*` | Push messaging for Amazon apps | — | keep | never: com.amazon.device.messaging |
| `com.ivona.*` | Text-to-speech (VoiceView accessibility) | — | keep | — |
| `com.svox.pico` | Text-to-speech (VoiceView accessibility) | — | keep | — |

## Where dumbtv and debloatfiretv differ

| Package | debloatfiretv | dumbtv | Why dumbtv does what it does |
|---|---|---|---|
| `com.amazon.vizzini` | safe (Alexa voice UI) | never | A persistent priv-app: it keeps running when disabled, and on some TVs covers the screen with "Unable to Detect Your Remote" (AGENTS.md, rule 9). `ALEXA=0` turns off the wake word and voice instead. |
| `com.amazon.storm.lightning.tutorial` | safe (onboarding tutorial) | never | Despite the name it holds the PIN screen the Fire TV phone app pairs with; disabled, the phone app cannot pair. |
| `com.amazon.tv.channelscan`, `com.vewd.core.*` | safe (tuner scan, HbbTV) | never | dumbtv runs on Fire TV Edition televisions with antennas and cable; those lose channel search and the red button. |
| `com.amazon.tv.forcedotaupdater.v2` | keep (system updates) | disabled | dumbtv files it under update nags. The updater itself (`com.amazon.device.software.ota`) is protected; the DNS filter blocks the update servers, and [the FAQ](FAQ.md) explains how to update on purpose. |
| `com.amazon.hedwig` | safe ("Amazon News") | disabled | dumbtv's list records it as watch-time and engagement reporting. Both agree it can go. |
| `com.amazon.alexadirectivebrokerservice`, `com.amazon.alexa.datastore.app` | keep (Alexa backend, used by Matter) | ALEXA=0 | Kept by default. Turning Alexa off takes them too, which also stops the TV's Matter controller. |
| `com.amazon.ftv.screensaver` | keep (protects a panel from burn-in) | if named | Only when named, and `debloat.sh` then points the TV at Android's own screensaver (when the TV has one) so it does not just go to sleep at the timeout. |

## Notes from the same research

- Privacy keys some tools write (`amazon:device_metrics_opt_in`, `amazon:acr_enabled`,
  `amazon:sidewalk_enabled`) do not exist on Fire OS 7.7.1.7: `settings get` answers
  `null`, so writing them does nothing. The keys that work are the ones in
  `data/fireos/settings.txt` (`amz_limit_ad_tracking`,
  `advertisingIdApp:interestBasedAds:value`, `USAGE_METRICS_UPLOAD_ENABLED`, ...).
- `adb exec-out screencap -p` on that TV prepends a log line ("Init wrapper sys
  mutex..."); strip everything before the PNG header to get a valid image.
- Mixed English and German in Settings there was not caused by debloating: Fire OS
  renamed the top-level tiles, and the German overlay only translates the old names.
