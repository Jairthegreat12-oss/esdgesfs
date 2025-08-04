/*
================================================================================
||                                                                            ||
||                           GAME CLIENT (C# - Unity Style)                     ||
||                                                                            ||
================================================================================

This C# code simulates how a game client (like one made in Unity or Godot)
would handle both the license key validation and the mod loading.

--------------------------------------------------------------------------------
-- File: GameManager.cs
--------------------------------------------------------------------------------
*/

using System;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using System.Collections.Generic;
// This would typically be a JSON library like Newtonsoft.Json or Unity's JsonUtility
// For this example, we'll simulate it with a simple dictionary.
using SimpleJson; 

public class GameManager
{
    // --- License System Variables ---
    private static readonly HttpClient httpClient = new HttpClient();
    private const string API_URL = "http://127.0.0.1:5000/validate_key"; // Our local Python server
    private const string LICENSE_FILE = "license.dat";
    public bool IsLicensed { get; private set; } = false;

    // --- Modding System Variables ---
    public Dictionary<string, Item> gameItems = new Dictionary<string, Item>();
    private string modsPath = "Mods";

    // --- Game Entry Point ---
    public async Task Start()
    __p_
        Console.WriteLine("--- Starting Game ---");
        await CheckLicense();

        if (IsLicensed)
        {
            Console.WriteLine("License is valid. Welcome!");
            InitializeGameData();
            LoadMods();
            DisplayGameItems();
        }
        else
        {
            Console.WriteLine("This game requires a valid license key to play.");
            // In a real game, you would show a UI prompt to enter a key.
            // We'll simulate entering a key from the console.
            Console.Write("Enter license key: ");
            string key = Console.ReadLine();
            await ValidateKey(key);
            if(IsLicensed) {
                 // Relaunch or continue
                 Console.WriteLine("Key accepted! Please restart the game.");
            } else {
                 Console.WriteLine("Invalid key. Exiting.");
            }
        }
    }

    // --- License System Methods ---
    private async Task CheckLicense()
    {
        if (File.Exists(LICENSE_FILE))
        {
            string key = File.ReadAllText(LICENSE_FILE);
            await ValidateKey(key);
        }
    }

    private async Task ValidateKey(string key)
    {
        try
        {
            var response = await httpClient.GetStringAsync($"{API_URL}?key={key}");
            // In a real scenario, you'd parse a JSON response.
            if (response.Contains("\"status\": \"valid\""))
            {
                IsLicensed = true;
                File.WriteAllText(LICENSE_FILE, key); // Save the valid key
            }
            else
            {
                IsLicensed = false;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error validating key: {ex.Message}");
            IsLicensed = false;
        }
    }

    // --- Modding System Methods ---
    private void InitializeGameData()
    {
        Console.WriteLine("\n--- Loading Base Game Data ---");
        // In a real game, this would be loaded from a base 'data.json' file
        gameItems.Add("stone_pickaxe", new Item { Name = "Stone Pickaxe", Power = 5 });
        gameItems.Add("iron_shovel", new Item { Name = "Iron Shovel", Power = 3 });
    }

    private void LoadMods()
    {
        Console.WriteLine("\n--- Loading Mods ---");
        if (!Directory.Exists(modsPath))
        {
            Console.WriteLine("Mods folder not found. No mods will be loaded.");
            Directory.CreateDirectory(modsPath);
            return;
        }

        foreach (var directory in Directory.GetDirectories(modsPath))
        {
            string modName = new DirectoryInfo(directory).Name;
            string itemsFile = Path.Combine(directory, "items.json");
            if (File.Exists(itemsFile))
            {
                Console.WriteLine($"Found mod: {modName}");
                string json = File.ReadAllText(itemsFile);
                
                // Using a simulated JSON parser
                var modItems = SimpleJson.DeserializeObject<Dictionary<string, Item>>(json);

                foreach(var modItem in modItems)
                {
                    if(gameItems.ContainsKey(modItem.Key))
                    {
                        Console.WriteLine($"  - Overwriting item: {modItem.Key}");
                        gameItems[modItem.Key] = modItem.Value;
                    }
                    else
                    {
                        Console.WriteLine($"  - Adding new item: {modItem.Key}");
                        gameItems.Add(modItem.Key, modItem.Value);
                    }
                }
            }
        }
    }
    
    private void DisplayGameItems()
    {
        Console.WriteLine("\n--- Final Game Items ---");
        foreach(var item in gameItems)
        {
            Console.WriteLine($" - ID: {item.Key}, Name: {item.Value.Name}, Power: {item.Value.Power}");
        }
    }
}

// Helper classes to simulate game data and JSON parsing
public class Item
{
    public string Name { get; set; }
    public int Power { get; set; }
}

// Dummy JSON parser for demonstration purposes
namespace SimpleJson
{
    public static class SimpleJson
    {
        public static T DeserializeObject<T>(string json)
        {
            // This is a placeholder for a real JSON library like Newtonsoft.Json
            // It's not a real parser.
            var dict = new Dictionary<string, Item>();
            if(json.Contains("diamond_pickaxe")) {
                 dict.Add("diamond_pickaxe", new Item { Name = "Diamond Pickaxe", Power = 20 });
            }
            if(json.Contains("stone_pickaxe")) {
                 dict.Add("stone_pickaxe", new Item { Name = "Stone Pickaxe", Power = 7 });
            }
            return (T)Convert.ChangeType(dict, typeof(T));
        }
    }
}

// --- Program Entry ---
public class Program
{
    public static async Task Main(string[] args)
    {
        var gameManager = new GameManager();
        await gameManager.Start();
    }
}
