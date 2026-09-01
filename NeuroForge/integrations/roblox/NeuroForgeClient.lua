local HttpService = game:GetService("HttpService")

local NeuroForgeClient = {}
NeuroForgeClient.Endpoint = "http://127.0.0.1:8000/chat"

function NeuroForgeClient.Chat(message, sessionId)
    local body = HttpService:JSONEncode({
        message = message,
        session_id = sessionId or "roblox"
    })

    local response = HttpService:RequestAsync({
        Url = NeuroForgeClient.Endpoint,
        Method = "POST",
        Headers = { ["Content-Type"] = "application/json" },
        Body = body
    })

    if not response.Success then
        error("NeuroForge API request failed: " .. tostring(response.StatusCode))
    end

    return HttpService:JSONDecode(response.Body)
end

return NeuroForgeClient
