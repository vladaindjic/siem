package rs.ac.uns.ftn.siem.web;

import javax.net.ssl.*;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketAddress;
import java.net.SocketTimeoutException;
import java.nio.ByteBuffer;
import java.security.KeyStore;
import java.util.List;

public class DTLSUdpConsumer {

//    void handshake(SSLEngine engine, DatagramSocket socket, SocketAddress peerAddr) throws Exception {
//        boolean endLoops = false;
//        // private static int MAX_HANDSHAKE_LOOPS = 60;
//        int loops = MAX_HANDSHAKE_LOOPS;
//        engine.beginHandshake();
//        while (!endLoops && (serverException == null) && (clientException == null)) {
//            if (--loops < 0) {
//                throw new RuntimeException("Too many loops to produce handshake packets");
//            }
//            SSLEngineResult.HandshakeStatus hs = engine.getHandshakeStatus();
//            if (hs == SSLEngineResult.HandshakeStatus.NEED_UNWRAP ||
//                    hs == SSLEngineResult.HandshakeStatus.NEED_UNWRAP_AGAIN) {
//                ByteBuffer iNet;
//                ByteBuffer iApp;
//                if (hs == SSLEngineResult.HandshakeStatus.NEED_UNWRAP) {
//                    // Receive ClientHello request and other SSL/TLS/DTLS records
//                    byte[] buf = new byte[1024];
//                    DatagramPacket packet = new DatagramPacket(buf, buf.length);
//                    try {
//                        socket.receive(packet);
//                    } catch (SocketTimeoutException ste) {
//                        // Retransmit the packet if timeout
//                        List <Datagrampacket> packets = onReceiveTimeout(engine, peerAddr);
//                        for (DatagramPacket p : packets) {
//                            socket.send(p);
//                        }
//                        continue;
//                    }
//                    iNet = ByteBuffer.wrap(buf, 0, packet.getLength());
//                    iApp = ByteBuffer.allocate(1024);
//                } else {
//                    iNet = ByteBuffer.allocate(0);
//                    iApp = ByteBuffer.allocate(1024);
//                }
//                SSLEngineResult r = engine.unwrap(iNet, iApp);
//                SSLEngineResult.Status rs = r.getStatus();
//                hs = r.getHandshakeStatus();
//                if (rs == SSLEngineResult.Status.BUFFER_OVERFLOW) {
//                    // The client maximum fragment size config does not work?
//                    throw new Exception("Buffer overflow: " +
//                            "incorrect client maximum fragment size");
//                } else if (rs == SSLEngineResult.Status.BUFFER_UNDERFLOW) {
//                    // Bad packet, or the client maximum fragment size
//                    // config does not work?
//                    if (hs != SSLEngineResult.HandshakeStatus.NOT_HANDSHAKING) {
//                        throw new Exception("Buffer underflow: " +
//                                "incorrect client maximum fragment size");
//                    } // Otherwise, ignore this packet
//                } else if (rs == SSLEngineResult.Status.CLOSED) {
//                    endLoops = true;
//                } // Otherwise, SSLEngineResult.Status.OK
//                if (rs != SSLEngineResult.Status.OK) {
//                    continue;
//                }
//            } else if (hs == SSLEngineResult.HandshakeStatus.NEED_WRAP) {
//                // Call a function to produce handshake packets
//                List<DatagramPacket> packets = produceHandshakePackets(engine, peerAddr);
//                for (DatagramPacket p : packets) {
//                    socket.send(p);
//                }
//            } else if (hs == SSLEngineResult.HandshakeStatus.NEED_TASK) {
//                runDelegatedTasks(engine);
//            } else if (hs == SSLEngineResult.HandshakeStatus.NOT_HANDSHAKING) {
//                // OK, time to do application data exchange
//                endLoops = true;
//            } else if (hs == SSLEngineResult.HandshakeStatus.FINISHED) {
//                endLoops = true;
//            }
//        }
//        SSLEngineResult.HandshakeStatus hs = engine.getHandshakeStatus();
//        if (hs != SSLEngineResult.HandshakeStatus.NOT_HANDSHAKING) {
//            throw new Exception("Not ready for application data yet");
//        }
//    }




    public static void main(String args[]) throws Exception{

        SSLContext sslContext;
        String hostname = "";
        int port = 33333;

        // Create and initialize the SSLContext with key material
        char[] passphrase = "vladimir".toCharArray();

        // First initialize the key and trust material
        KeyStore ksKeys = KeyStore.getInstance("PKCS12");
        ksKeys.load(new FileInputStream("src/main/resources/boot.p12"), passphrase);
        KeyStore ksTrust = KeyStore.getInstance("PKCS12");
        ksTrust.load(new FileInputStream("src/main/resources/myCA.p12"), passphrase);

        // KeyManagers decide which key material to use
        KeyManagerFactory kmf = KeyManagerFactory.getInstance("PKIX");
        kmf.init(ksKeys, passphrase);

        // TrustManagers decide whether to allow connections
        TrustManagerFactory tmf = TrustManagerFactory.getInstance("PKIX");
        tmf.init(ksTrust);

        // Get an SSLContext for DTLS Protocol without authentication
        sslContext = SSLContext.getInstance("DTLS");
        sslContext.init(null, null, null);

        // Create the engine
        SSLEngine engine = sslContext.createSSLEngine(hostname, port);

        // Use the engine as server
        engine.setUseClientMode(false);

        // Require client authentication
        engine.setNeedClientAuth(true);

        System.out.println("Cao, svete!");
    }
}
