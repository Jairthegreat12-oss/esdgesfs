-- Place this script where server scripts are run.

local SIT_ANIMATION_ID = "rbxassetid://123456789" -- Replace with your sit animation ID

game.Players.PlayerAdded:Connect(function(player)
    player.Chatted:Connect(function(message)
        if string.lower(message) == "/sit" then
            local character = player.Character
            if character and character:FindFirstChild("Humanoid") then
                local humanoid = character.Humanoid
                
                -- Create and play the animation
                local sitAnim = Instance.new("Animation")
                sitAnim.AnimationId = SIT_ANIMATION_ID
                
                local animTrack = humanoid:LoadAnimation(sitAnim)
                animTrack:Play()
            end
        end
    end)
end)
