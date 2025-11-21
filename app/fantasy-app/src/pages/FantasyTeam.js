import React, { useEffect, useState } from "react";
import "./FantasyTeam.css";
import { api_network, local_api_network } from "../App";

export default function FantasyTeam({ userID }) {
  
  const [team, setTeam] = useState(null);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [captainMenuOpen, setCaptainMenuOpen] = useState(false);


  useEffect(() => {
    async function load() {
      const t = await get_team(userID);
      setTeam(t);
    }
    load();
  }, [userID]);


  async function get_team(userID) {
    try {
      const response = await fetch(api_network + "/fetch_team", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userID }),
      });

      if(response.ok) {
        const data = await response.json();
        return data;         
      }
      else {
        const err = await response.json()
        console.log(err)
      }
    } catch (err) {
      console.error(err);
      alert("Team load failed");
    }
  }

  if (!team) return <p href = "/transfers" >No Team associated with user. Create a Team First in "Transfers"</p>;

  const formationRows = [
    { label: "Goalkeeper", key: "goalkeeper" },
    { label: "Defenders", key: "defenders" },
    { label: "Midfielders", key: "midfielders" },
    { label: "Forwards", key: "forwards" },
  ];

  // Immutable safe swap: bench <-> field only
  // helper: map player.position to team group key
function getGroupKeyByPosition(position) {
  const pos = (position || "").toUpperCase();
  if (pos === "G") return "goalkeeper";
  if (pos === "D") return "defenders";
  if (pos === "M") return "midfielders";
  if (pos === "F") return "forwards";
  // default fallback:
  return "midfielders";
}


function makeCaptain(player) {
  const newTeam = {
    goalkeeper: [...team.goalkeeper],
    defenders: [...team.defenders],
    midfielders: [...team.midfielders],
    forwards: [...team.forwards],
    substitutes: [...team.substitutes],
  };

  // Remove captain from anyone who currently has it
  for (const group of ["goalkeeper", "defenders", "midfielders", "forwards", "substitutes"]) {
    newTeam[group] = newTeam[group].map(p => ({
      ...p,
      captain: false
    }));
  }

  // Assign captain to selected player
  const g = getGroupKeyByPosition(player.position);
  newTeam[g] = newTeam[g].map(p =>
    p.player_id === player.player_id ? { ...p, captain: true } : p
  );

  setTeam(newTeam);
  setCaptainMenuOpen(false);
  setSelectedPlayer(null);
}


function handlePlayerClick(player, groupKey) {

  // Captain selection
  // If clicking a field player, allow captain selection:
  if (groupKey !== "substitutes") {
    setSelectedPlayer({ player, groupKey });
    setCaptainMenuOpen(true);
  } else {
    setCaptainMenuOpen(false);
  }


  if (!selectedPlayer) {
    setSelectedPlayer({ player, groupKey });
    return;
  }

  const first = selectedPlayer;
  const second = { player, groupKey };

  const isBenchFirst = first.groupKey === "substitutes";
  const isBenchSecond = second.groupKey === "substitutes";

  // Only allow bench <-> field swaps
  if (isBenchFirst === isBenchSecond) {
    setSelectedPlayer(null);
    return;
  }

  const bench = isBenchFirst ? first : second;
  const field = isBenchFirst ? second : first;

  // Clone state immutably
  const newTeam = {
    goalkeeper: [...team.goalkeeper],
    defenders: [...team.defenders],
    midfielders: [...team.midfielders],
    forwards: [...team.forwards],
    substitutes: [...team.substitutes],
  };

  // --- Remove players from their old groups ---
  newTeam.substitutes = newTeam.substitutes.filter((p) => p.player_id !== bench.player.player_id);
  newTeam[field.groupKey] = newTeam[field.groupKey].filter((p) => p.player_id !== field.player.player_id);

  // --- Add players to their new groups ---
  // field player goes to bench
  newTeam.substitutes.push(field.player);

  // bench player goes to their correct positional group
  const benchTargetGroup = getGroupKeyByPosition(bench.player.position);
  newTeam[benchTargetGroup].push(bench.player);

  // --- VALIDATION CHECKS ---
  // 1. Prevent less than 3 defenders
  if (newTeam.defenders.length < 3) {
    alert("You must have at least 3 defenders on the field.");
    setSelectedPlayer(null);
    return;
  }

  // 2. Prevent more or less than 1 goalkeeper
  if (newTeam.goalkeeper.length !== 1) {
    alert("You must have exactly 1 goalkeeper on the field.");
    setSelectedPlayer(null);
    return;
  }

  // Swap captain if needed
  if (field.player.captain === true || bench.player.captain === true) {
    // Remove captain from everyone first
    for (const group of ["goalkeeper", "defenders", "midfielders", "forwards", "substitutes"]) {
      newTeam[group] = newTeam[group].map(p => ({ ...p, captain: false }));
    }

    // Whichever player ends on the FIELD should be the captain
    const finalFieldGroup = getGroupKeyByPosition(bench.player.position);

    newTeam[finalFieldGroup] = newTeam[finalFieldGroup].map(p =>
      p._player_id === bench.player.player_id ? { ...p, captain: true } : p
    );
  }

  // If valid -> apply update
  setTeam(newTeam);
  setSelectedPlayer(null);
}



  async function saveTeam() {
    try {
      const resp = await fetch("http://127.0.0.1:8000/save_team", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userID, team }),
      });
      if (!resp.ok) throw new Error("Save failed");
      alert("Team saved");
    } catch (err) {
      console.error(err);
      alert("Save failed");
    }
  }

  return (
    <>
    <div className="container">
    <div className="fantasy-team-container">
      <h1>My Team</h1>
      {/* Captain */}
      {captainMenuOpen && selectedPlayer && selectedPlayer.groupKey !== "substitutes" && (
      <div className="captain-controls">
        <p>Selected: {selectedPlayer.player.player}</p>
        <button
          className="captain-button"
          onClick={() => makeCaptain(selectedPlayer.player)}
        >
          Make Captain
        </button>
        <button
          className="cancel-button"
          onClick={() => { setSelectedPlayer(null); setCaptainMenuOpen(false); }}
        >
          Cancel
        </button>
      </div>
      )}


      {/* Pitch: each row uses CSS variable --n for columns */}
      <div className="pitch">
        {formationRows.map((row) => {
          return (
            <div
              className="pitch-line"
              key={row.key}
            >
              {team[row.key].map((player) => (
                <button
                  key={player.player_id}
                  className={`player-slot ${selectedPlayer?.player.player_id === player.player_id ? "selected" : ""}`}
                  onClick={() => handlePlayerClick(player, row.key)}
                >
                  <div className="slot-name">{player.player}</div>
                  <div className="slot-pos">{player.position}</div>
                  <div className="captain">{player.captain ? <>&copy;</> : ""}</div>

                </button>
              ))}
            </div>
          );
        })}
      </div>

      {/* Bench */}
      <h2>Bench</h2>
      <div className="bench-row">
        {team.substitutes.map((player) => (
          <button
            key={player.player_id}
            className={`bench-slot ${selectedPlayer?.player.player_id === player.player_id ? "selected" : ""}`}
            onClick={() => handlePlayerClick(player, "substitutes")}
          >
            <div className="slot-name">{player.player}</div>
            <div className="slot-pos">{player.position}</div>
          </button>
        ))}
      </div>

      <button className="save-button" onClick={saveTeam}>
        Save Team
      </button>
    </div>
    <div className="game-list-container">
      <h1>Matchweek #</h1>
    </div>
    </div>
    </>
  );
}