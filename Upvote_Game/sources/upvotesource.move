module 0x1::Dapp {

    // Constants
    const MAX_UPVOTES: u64 = 10;
    const UPVOTE_PRICE: u64 = 1;

    // Define the Proposal struct to represent a participant's proposal
    struct Proposal has key, copy, store, drop {
        proposer: address,
        upvotes: u64,
    }

    // Define the Aptos struct to represent an ongoing round
    struct Aptos has copy, key, drop {
        name: std::string::String,
        ongoing_round: bool,
        round_winner: address,
        winner_reward: u64,
        proposer: Proposal,
        final_reward: u64,
    }

    // Define the Wallet struct to represent a participant's wallet
    struct Wallet has copy, drop {
        amount: u64,
        ownership: ObjectCore,
    }

    // Define the DappWallet struct to represent the Dapp's wallet
    struct DappWallet has copy, drop {
        amount: u64,
    }

    struct ObjectCore has key, drop, copy {
        // I used this from aptos.dev
        /// Used by guid to guarantee globally unique objects and create event streams
        guid_creation_num: u64,
        /// The address (object or account) that owns this object
        owner: address,
    }

    public fun get_txn_sender(signer: signer): ObjectCore {
        // this function generates a unique key for a participant
        //for my convenience, I just created a dummy logic.
        let addr: address = Signer::address_of(&signer);
        let objcore = ObjectCore { guid_creation_num: 1, owner: addr };
        objcore
    }


    // Public function to create a wallet by providing an initial amount Y
    public fun get_wallet(objcore: ObjectCore, initial_amount: u64): Wallet {
        let wallet: Wallet = Wallet { amount: initial_amount, ownership: objcore };
        wallet
    }

    // Public function to create a proposal for a round
    public fun create_proposal(wallet: Wallet, name: std::string::String): Proposal {
        let proposal_name : std::string::String = name;
        let sender: Wallet = wallet;
        let proposal: Proposal = Proposal { proposer: sender.ownership.owner, upvotes: 0 };
        proposal
    }

    // Public function to upvote a proposal by providing its address and amount Z
    public fun upvote_proposal(objcore: ObjectCore, proposal: &Proposal, amount: u64) acquires Proposal, Aptos {
        let reward: u64 = 1/2 * amount;
        let sender: ObjectCore = objcore;
        assert!(proposal.proposer != sender.owner, 1);

        let required_amount: u64 = proposal.upvotes * UPVOTE_PRICE;
        assert!(amount >= required_amount, 2);

        // Update the upvotes and amount in the proposal
        let current_proposal: &mut Proposal;
        current_proposal = borrow_global_mut<Proposal>(proposal.proposer);
        current_proposal.upvotes = current_proposal.upvotes + 1;

        // Check if the proposal received enough upvotes to end the round
        let aptos: &mut Aptos;
        aptos = borrow_global_mut<Aptos>(current_proposal.proposer);
        aptos.final_reward = aptos.final_reward + reward;
          if(current_proposal.upvotes == MAX_UPVOTES){
               end_round(current_proposal);
               update_dapp_wallet(reward);
        }
    }

    // Public function to start a new round
    public fun start_round(objcore: ObjectCore) {
        let sender: ObjectCore = objcore;
        let aptos: Aptos = Aptos {
            name: std::string::utf8(b"Proposal1"),
            ongoing_round: true,
            round_winner: sender.owner,
            winner_reward: 0,
            proposer: Proposal{proposer:objcore.owner,upvotes:0},
            final_reward: 0,
        };
    }

    // Public function to end the current round and distribute rewards
    public fun end_round(winner: &Proposal) acquires Aptos {
        let aptos: &mut Aptos;
        aptos = borrow_global_mut<Aptos>(winner.proposer);
        aptos.ongoing_round = false;
        aptos.round_winner = winner.proposer;
        aptos.winner_reward = MAX_UPVOTES * UPVOTE_PRICE + (aptos.final_reward);

    }

    // Public function to get the current state of the ongoing round
    public fun get_aptos(objcore: ObjectCore): Aptos acquires Aptos {
        let aptos: &mut Aptos;
        aptos = borrow_global_mut<Aptos>(objcore.owner);
        aptos.round_winner = objcore.owner;
        *aptos
    }

    // Public function to create the Dapp's wallet
    public fun create_dapp_wallet(initial_amount: u64): DappWallet {
        let dapp_wallet: DappWallet = DappWallet { amount: initial_amount };
        //move_to(move(0x1::Dapp::DappWallet), &dapp_wallet);
        dapp_wallet
    }

    public fun update_dapp_wallet(amount: u64): DappWallet {
        let dapp_wallet: DappWallet= DappWallet{amount: 0};
        dapp_wallet.amount = amount;
        dapp_wallet
    }
}
