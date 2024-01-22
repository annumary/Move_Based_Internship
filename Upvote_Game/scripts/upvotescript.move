script {
  use 0x1::Dapp;
  use 0x1::Dapp::ObjectCore;

  fun master (account: signer) {
    let participant_account = account;
    // Initialize Dapp's wallet with an initial amount
    let dapp_wallet: Dapp::DappWallet = Dapp::create_dapp_wallet(100);

    // Participant creates a wallet with an initial amount Y
    let participant_address = Dapp::get_txn_sender(participant_account);
    let participant1_wallet: Dapp::Wallet = Dapp::get_wallet(participant_address, 50);

    // Participant  starts a round
    Dapp::start_round(copy participant_address);

    // Participant creates a proposal for the ongoing round
    let vect: vector<u8> = b"Proposal1";
    let str: std::string::String = std::string::utf8(vect);
    let proposal1: Dapp::Proposal = Dapp::create_proposal(participant1_wallet, str );

    // Participant 2 upvotes the proposal1 with an amount Z
    let z: u64 = 10;
    Dapp::upvote_proposal(copy participant_address, &proposal1, z);
    // instead of participant_address, it should be address of the proposal object
    // for simplicity, I assume both are same.

    // Check the current state of the ongoing round
    let aptos_state: Dapp::Aptos = Dapp::get_aptos(copy participant_address);

    // Participant 1 ends the ongoing round
    Dapp::end_round(&proposal1);

    // Check the current state after ending the round
    let updated_aptos_state: Dapp::Aptos = Dapp::get_aptos(copy participant_address);
  }
}