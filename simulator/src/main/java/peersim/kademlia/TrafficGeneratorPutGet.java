package peersim.kademlia;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import peersim.config.Configuration;
import peersim.core.CommonState;
import peersim.core.Control;
import peersim.core.Network;
import peersim.core.Node;
import peersim.edsim.EDSimulator;

import java.util.concurrent.ThreadLocalRandom;
import java.util.HexFormat;

/**
 * This control generates random search traffic from nodes to random destination
 * node.
 *
 * @author Daniele Furlan, Maurizio Bonani
 * @version 1.0
 */

// ______________________________________________________________________________________________
public class TrafficGeneratorPutGet implements Control {

  // ______________________________________________________________________________________________
  /** MSPastry Protocol to act */
  private static final String PAR_PROT = "protocol";
  private static final String PAR_RPS = "requests_per_second";

  /** MSPastry Protocol ID to act */
  private final int pid;

  // ______________________________________________________________________________________________
  public TrafficGeneratorPutGet(String prefix) {
    pid = Configuration.getPid(prefix + "." + PAR_PROT);
  }

  // Generate a random identifier to look up
  private String GenerateRandIdentifier(int idLength) {
    byte[] randomBytes = new byte[idLength];
    ThreadLocalRandom.current().nextBytes(randomBytes);
    String hexIdentifier = HexFormat.of().formatHex(randomBytes);
    return hexIdentifier;
  }

  // ______________________________________________________________________________________________
  /**
   * Generates a PUT message for t1 key and string message
   *
   * @return Message
   */
  private Message generatePutMessage() {

    // Existing active destination node
    MessageDigest digest;
    BigInteger id;
    String topic = GenerateRandIdentifier(2);
    String value = topic;
    // Check the cache first, otherwise perform a standard lookup
    // Ignore the cache here for this branch `Collision`
    // checkCache(topic);
    try {
      digest = MessageDigest.getInstance("SHA-256");
      byte[] hash = digest.digest(topic.getBytes(StandardCharsets.UTF_8));
      id = new BigInteger(1, hash);
      Message m = Message.makeInitPutValue(id, value);
      m.timestamp = CommonState.getTime();
      // System.out.println("Put message " + m.body + " " + m.value);
      return m;
    } catch (NoSuchAlgorithmException e) {
      e.printStackTrace();
      return null;
    }
  }

  // ______________________________________________________________________________________________
  /**
   * Generates a GET message for t1 key.
   *
   * @return Message
   */
  private Message generateGetMessage() {
    MessageDigest digest;
    BigInteger id;
    try {
      String topic = GenerateRandIdentifier(1);
      // String topic = "t1";
      digest = MessageDigest.getInstance("SHA-256");
      byte[] hash = digest.digest(topic.getBytes(StandardCharsets.UTF_8));
      id = new BigInteger(1, hash);
      Message m = Message.makeInitGetValue(id);
      m.timestamp = CommonState.getTime();

      return m;
    } catch (NoSuchAlgorithmException e) {
      e.printStackTrace();
      return null;
    }
  }
  // JA - If it is in the cache, log collison and exit simulation.
  // JA - keep the logs in the same format to make measuring easier.
  private void checkCache(String ident) {
    int identInt = Integer.parseInt(ident, 16);
    if (KademliaObserver.bitSetIdentUpdated.get(identInt) == true) {
      System.out.printf("Key already inBitmap: %s detected at %s\n", ident, CommonState.getTime());
      // Exit the simulation early
      System.exit(0);
    }

  }

  // ______________________________________________________________________________________________
  /**
   * Every call of this control generates and send a random find node message
   *
   * @return boolean
   */
  public boolean execute() {

    Node start;
    do {
      start = Network.get(CommonState.r.nextInt(Network.size()));
    } while ((start == null) || (!start.isUp()));

    // if (first) {
    // EDSimulator.add(0, generatePutMessage(), start, pid);
    // EDSimulator.add(0, generatePutMessage(), start, pid);
    // first = false;
    // } else {
    // EDSimulator.add(0, generateGetMessage(), start, pid);
    // }

    EDSimulator.add(0, generatePutMessage(), start, pid);
    // System.out.printf("ACTUAL bits set: %d\n", KademliaObserver.bitSetIdentifiers.cardinality());

    return false;
  }

  // ______________________________________________________________________________________________

} // End of class
// ______________________________________________________________________________________________
