"""
Written by Gothrand
This script is designed to assist speedrunners running 100%, mainly by keeping track of 
unlocks such as logs and achievements by checking the user profile that is created for the 
purpose of running the category for edits in real time.

Instructions to use the file pending.
"""
import os, shutil, glob
import xml.etree.ElementTree as ET
from time import sleep

# achievements and logs lists
logs = [
    "Logs.WispBody",
    "Logs.JellyfishBody",
    "Logs.BeetleBody",
    "Logs.LemurianBody",
    "Logs.HermitCrabBody",
    "Logs.ImpBody",
    "Logs.VultureBody",
    "Logs.RoboBallMiniBody",
    "Logs.MiniMushroom",
    "Logs.BellBody",
    "Logs.BeetleGuardBody",
    "Logs.BisonBody",
    "Logs.GolemBody",
    "Logs.ClayBruiserBody",
    "Logs.GreaterWispBody",
    "Logs.LemurianBruiserBody",
    "Logs.Parent",
    "Logs.Nullifier",
    "Logs.BeetleQueenBody",
    "Logs.ClayBossBody",
    "Logs.TitanBody",
    "Logs.MagmaWormBody",
    "Logs.VagrantBody",
    "Logs.ImpBossBody",
    "Logs.GravekeeperBody",
    "Logs.RoboBallBossBody",
    "Logs.Scav",
    "Logs.ElectricWormBody",
    "Logs.SuperRoboBallBossBody",
    "Logs.TitanGoldBody",
    "Logs.LunarWisp",
    "Logs.LunarGolem",
    "Logs.BrotherBod",
    "Logs.Stages.blackbeach",
    "Logs.Stages.golemplains",
    "Logs.Stages.foggyswamp",
    "Logs.Stages.goolake",
    "Logs.Stages.frozenwall",
    "Logs.Stages.wispgraveyard",
    "Logs.Stages.dampcavesimple",
    "Logs.Stages.shipgraveyard",
    "Logs.Stages.skymeadow",
    "Logs.Stages.goldshores",
    "Logs.Stages.arena",
    "Logs.Stages.bazaar",
    "Logs.Stages.limbo",
    "Logs.Stages.artifactworld",
    "Logs.Stages.mysteryspace",
    "Logs.Stages.moon",
    "Logs.Stages.rootjungle"
]

achievements = [
    "RepeatedleyDuplicateItems",
    "KillEliteMonster",
    "KillBossQuick",
    "FailShrineChance",
    "Discover10UniqueTier1",
    "Die5Times",
    "CompleteTeleporterWithoutInjury",
    "CompleteTeleporter",
    "AttackSpeed",
    "MultiCombatShrine",
    "MoveSpeed",
    "KillTotalEnemies",
    "KillElitesMilestone",
    "Discover5Equipment",
    "CompletePrismaticTrial",
    "KillElementalLemurians",
    "ChargeTeleporterWhileNearDeath",
    "AutomationActivation",
    "Complete20Stages",
    "HardEliteBossKill",
    "StayAlive1",
    "CompleteThreeStagesWithoutHealing",
    "HardHitter",
    "FindDevilAltar",
    "LoopOnce",
    "CompleteMainEndingHard",
    "SuicideHermitCrabs",
    "NeverBackDown",
    "KillBossQuantityInRun",
    "CarryLunarItems",
    "UseThreePortals",
    "MajorMultikill",
    "BurnToDeath",
    "TotalDronesRepaired",
    "TotalMoneyCollected",
    "FindTimedChest",
    "KillGoldTitanInOneCycle",
    "MaxHealingShrine",
    "LogCollector",
    "CompleteMultiBossShrine",
    "CleanupDuty",
    "Die20Times",
    "CompleteThreeStages",
    "RepeatFirstTeleporter",
    "Complete30StagesCareer",
    "FreeMage",
    "CompleteUnknownEnding",
    "RescueTreebot",
    "DefeatSuperRoboBallBoss",
    "BeatArena",
    "CompleteMainEnding",
    "ObtainArtifactSwarms",
    "ObtainArtifactEliteOnly",
    "ObtainArtifactBomb",
    "ObtainArtifactCommand",
    "ObtainArtifactEnigma",
    "ObtainArtifactGlass",
    "ObtainArtifactMixEnemy",
    "ObtainArtifactMonsterTeamGainsItems",
    "ObtainArtifactRandomSurvivorOnRespawn",
    "ObtainArtifactSacrifice",
    "ObtainArtifactShadowClone",
    "ObtainArtifactWispOnDeath",
    "ObtainArtifactWeakAssKnees",
    "ObtainArtifactTeamDeath",
    "ObtainArtifactSingleMonsterType",
    "ObtainArtifactFriendlyFire"
]

logs.sort()
achievements.sort()

obtainedLogs = []
obtainedAchievements = []

# function definitions

def parseXML(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return root

def main():
    lastUpdate = None
    userProfile = None
    userProfiles = glob.glob(r"C:\Program Files (x86)\Steam\userdata\*\632360\remote\UserProfiles\*.xml")
    name = input("Please input name of profile to use: ")
    print("Searching for profile "+name)

    for file in userProfiles:
        root = parseXML(file)
        profileName = root.findtext("name")
        # get last filechange time
        lastUpdate = os.stat(file).st_mtime
        if profileName == name:
            userProfile = file
            print("Found user profile "+name+"!")
            break
    else:
        print("Could not find a profile with matching name: "+name)

    print("Looking for achievements/logs...")
    # main loop.  Terminates when all logs and achievements are gotten.
    while(obtainedLogs != logs and obtainedAchievements != achievements):
        if os.stat(userProfile).st_mtime == lastUpdate:
            continue
        else:
            # give time for risk to save to the xml (could prolly lower this value)
            sleep(0.5)
            lastUpdate = os.stat(file).st_mtime
            root = parseXML(userProfile)
            achievementGets = root.findtext("achievementsList").split(" ")
            for item in achievementGets:
                if item not in obtainedAchievements:
                    obtainedAchievements.append(item)
                    print("Got achievement: "+item)

            logElements = root.findall(".//unlock")
            for element in logElements:
                temp = element.text.split('.')
                if element.text.startswith("Logs.Stages"):
                    if temp[0]+'.'+temp[1]+'.'+temp[2] not in obtainedLogs:
                        obtainedLogs.append(temp[0]+'.'+temp[1]+'.'+temp[2])
                        print("Got log: "+temp[2])
                elif element.text.startswith("Logs"):
                    if temp[0]+'.'+temp[1] not in obtainedLogs:
                        obtainedLogs.append(temp[0]+'.'+temp[1])
                        print("Got log: "+temp[1])
                else:
                    continue

            obtainedLogs.sort()
            obtainedAchievements.sort()


if __name__ == "__main__":
    main()
