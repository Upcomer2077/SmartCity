BACK_out_path = "../backend/consumer/src/consumer/"
SIM_out_path = "../simulator/broker/src/broker/"
.PHONY: proto_backend proto_sim
.DEFAULT_GOAL := help


help:
	@echo ""
	@echo "Available commands:"
	@echo "---------------------------------------------------------------------------"
	@echo "make proto_backend     - Generate proto output for backend
	@echo "make proto_sim         - Generate proto output for simulator
	@echo "make help              - Show this help message"
	@echo "---------------------------------------------------------------------------"
	@echo ""

proto_backend:
	protoc --python_out=$(BACK_out_path) --pyi_out=$(BACK_out_path) sensor_data.proto

proto_sim:
	protoc --python_out=$(SIM_out_path) --pyi_out=$(SIM_out_path) sensor_data.proto


	