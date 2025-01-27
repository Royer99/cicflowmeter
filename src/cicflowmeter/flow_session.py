import csv
from collections import defaultdict


from scapy.sessions import DefaultSession

from .features.context.packet_direction import PacketDirection
from .features.context.packet_flow_key import get_packet_flow_key
from .flow import Flow
from .apiClient import Request
from .onosClient import OnosClient

EXPIRED_UPDATE = 40
MACHINE_LEARNING_API = "http://localhost:8000/predict"
GARBAGE_COLLECT_PACKETS = 100
THRESHOLD = 10


class FlowSession(DefaultSession):
    """Creates a list of network flows."""

    def __init__(self, *args, **kwargs):
        self.flows = {}
        self.csv_line = 0
        self.ipTable = {}
        self.attack_flows = 0
        self.normal_flows = 0

        if self.output_mode == "flow":
            output = open(self.output_file, "w")
            self.csv_writer = csv.writer(output)

        self.packets_count = 0

        self.clumped_flows_per_label = defaultdict(list)

        super(FlowSession, self).__init__(*args, **kwargs)

    def toPacketList(self):
        # Sniffer finished all the packets it needed to sniff.
        # It is not a good place for this, we need to somehow define a finish signal for AsyncSniffer
        self.garbage_collect(None)
        return super(FlowSession, self).toPacketList()

    def on_packet_received(self, packet):
        count = 0
        direction = PacketDirection.FORWARD

        if self.output_mode != "flow":
            if "TCP" not in packet:
                return
            elif "UDP" not in packet:
                return

        try:
            # Creates a key variable to check
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))
        except Exception:
            return

        self.packets_count += 1

        # If there is no forward flow with a count of 0
        if flow is None:
            # There might be one of it in reverse
            direction = PacketDirection.REVERSE
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))

        if flow is None:
            # If no flow exists create a new flow
            direction = PacketDirection.FORWARD
            flow = Flow(packet, direction)
            packet_flow_key = get_packet_flow_key(packet, direction)
            self.flows[(packet_flow_key, count)] = flow

        elif (packet.time - flow.latest_timestamp) > EXPIRED_UPDATE:
            # If the packet exists in the flow but the packet is sent
            # after too much of a delay than it is a part of a new flow.
            expired = EXPIRED_UPDATE
            while (packet.time - flow.latest_timestamp) > expired:
                count += 1
                expired += EXPIRED_UPDATE
                flow = self.flows.get((packet_flow_key, count))

                if flow is None:
                    flow = Flow(packet, direction)
                    self.flows[(packet_flow_key, count)] = flow
                    break
        elif "F" in str(packet.flags):
            # If it has FIN flag then early collect flow and continue
            flow.add_packet(packet, direction)
            self.garbage_collect(packet.time)
            return

        flow.add_packet(packet, direction)

        if not self.url_model:
            GARBAGE_COLLECT_PACKETS = 10000
        GARBAGE_COLLECT_PACKETS = 10000
        if self.packets_count % GARBAGE_COLLECT_PACKETS == 0 or (
            flow.duration > 120 and self.output_mode == "flow"
        ):
            self.garbage_collect(packet.time)

    def get_flows(self) -> list:
        return self.flows.values()

    def garbage_collect(self, latest_time) -> None:
        # TODO: Garbage Collection / Feature Extraction should have a separate thread
        if not self.url_model:
            #print("Garbage Collection Began. Flows = {}".format(len(self.flows)))
            pass
        keys = list(self.flows.keys())
        for k in keys:
            flow = self.flows.get(k)

            if (
                latest_time is None
                or latest_time - flow.latest_timestamp > EXPIRED_UPDATE
                or flow.duration > 10
            ):
                # TODO: update aggreted features
                flow.update_aggregated_features()

                data = flow.get_data()

                request = Request(
                    data['flow_duration'],
                    data['fwd_header_len'],
                    data['bwd_header_len'],
                    #(data['fwd_header_len'] + data['bwd_header_len']),
                    data['tot_fwd_pkts'],
                    data['tot_bwd_pkts'],
                    #(data['tot_fwd_pkts'] + data['tot_bwd_pkts']),
                    data['fwd_pkts_s'],
                    data['bwd_pkts_s'],
                    data['flow_pkts_s'],
                    # data['minDuration'],
                    # data['maxDuration'],
                    # data['sumDuration'],
                    # data['meanDuration'],
                    # data['stdDuration'],
                    data['flow_iat_min'],
                    data['flow_iat_max'],
                    data['flow_iat_mean'],
                    data['flow_iat_std'],
                    3
                )

                response = request.apiCall()
                # print(type(response))
                # print(response)
                # printself(data)
                # formated result

                if(response["class"] == 1):
                    print(
                        f'Detected normal flow (class ID {response["class"]}, using ), Key(srcip: {data["src_ip"]}, srcport: {data["src_port"]}, dstip: {data["dst_ip"]}, dstport: {data["dst_port"]}, proto: {data["protocol"]})')
                    # print(self.threshold)
                    self.normal_flows += 1
                else:
                    self.attack_flows += 1
                    print(
                        f'Detected attack flow (class ID {response["class"]}, using ), Key(srcip: {data["src_ip"]}, srcport: {data["src_port"]}, dstip: {data["dst_ip"]}, dstport: {data["dst_port"]}, proto: {data["protocol"]})')
                    print(data["src_ip"])
                    # print(self.packets_count)
                    if(data["src_ip"] not in self.ipTable):
                        self.ipTable[data["src_ip"]] = 1
                    else:
                        self.ipTable[data["src_ip"]] += 1
                    # print(self.ipTable)
                    # print(self.threshold)
                    if(self.ipTable[data["src_ip"]] >= int(self.threshold)):
                        print("ONOS CALL")
                        OnosClient.block(self.onos_url, data["src_ip"])

                if self.csv_line == 0:
                    self.csv_writer.writerow(data.keys())

                self.csv_writer.writerow(data.values())
                self.csv_line += 1
                print("Nomal Flows: ", self.normal_flows, " Attack flows", self.attack_flows)
                del self.flows[k]
        if not self.url_model:
            #print("Garbage Collection Finished. Flows = {}".format(len(self.flows)))
            pass


def generate_session_class(output_mode, output_file, url_model, threshold, onos_url):
    print(threshold)
    return type(
        "NewFlowSession",
        (FlowSession,),
        {
            "output_mode": output_mode,
            "output_file": output_file,
            "url_model": url_model,
            "threshold": threshold,
            "onos_url": onos_url
        },
    )
