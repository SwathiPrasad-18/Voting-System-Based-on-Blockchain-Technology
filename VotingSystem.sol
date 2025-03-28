// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract VotingSystem {
    address public admin;
    bool public votingActive;

    struct Voter {
        bool isRegistered;
        bool hasVoted;
    }

    struct Candidate {
        string name;
        uint voteCount;
    }

    mapping(address => Voter) public voters;
    Candidate[] public candidates;

    event VoterRegistered(address voter);
    event CandidateAdded(string name);
    event VoteCasted(address voter, string candidate);
    event VotingStarted();
    event VotingStopped();
    event WinnerDeclared(string winner, uint votes);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    modifier onlyDuringVoting() {
        require(votingActive, "Voting is not active");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function registerVoter(address _voter) public onlyAdmin {
        require(!voters[_voter].isRegistered, "Voter already registered");
        voters[_voter] = Voter(true, false);
        emit VoterRegistered(_voter);
    }

    function addCandidate(string memory _name) public onlyAdmin {
        candidates.push(Candidate(_name, 0));
        emit CandidateAdded(_name);
    }

    function startVoting() public onlyAdmin {
        require(!votingActive, "Voting is already active");
        votingActive = true;
        emit VotingStarted();
    }

    function stopVoting() public onlyAdmin {
        require(votingActive, "Voting is not active");
        votingActive = false;
        emit VotingStopped();
        declareWinner();
    }

    function vote(uint _candidateIndex) public onlyDuringVoting {
        require(voters[msg.sender].isRegistered, "You are not a registered voter");
        require(!voters[msg.sender].hasVoted, "You have already voted");
        require(_candidateIndex < candidates.length, "Invalid candidate index");

        voters[msg.sender].hasVoted = true;
        candidates[_candidateIndex].voteCount++;
        emit VoteCasted(msg.sender, candidates[_candidateIndex].name);
    }

    function declareWinner() private {
        require(!votingActive, "Voting is still active");

        uint maxVotes = 0;
        string memory winnerName;

        for (uint i = 0; i < candidates.length; i++) {
            if (candidates[i].voteCount > maxVotes) {
                maxVotes = candidates[i].voteCount;
                winnerName = candidates[i].name;
            }
        }
        emit WinnerDeclared(winnerName, maxVotes);
    }

    function getCandidates() public view returns (Candidate[] memory) {
        return candidates;
    }
}
