class Torrent:
    def __init__(self, data):
        self.added_on = None
        self.amount_left = None
        self.auto_tmm = None
        self.category = None
        self.completed = None
        self.completion_on = None
        self.dl_limit = None
        self.dlspeed = None
        self.downloaded = None
        self.downloaded_session = None
        self.eta = None
        self.f_l_piece_prio = None
        self.force_start = None
        self.hash = None
        self.last_activity = None
        self.magnet_uri = None
        self.max_ratio = None
        self.max_seeding_time = None
        self.name = None
        self.num_complete = None
        self.num_incomplete = None
        self.num_leechs = None
        self.num_seeds = None
        self.priority = None
        self.progress = None
        self.ratio = None
        self.ratio_limit = None
        self.save_path = None
        self.seeding_time_limit = None
        self.seen_complete = None
        self.seq_dl = None
        self.size = None
        self.state = None
        self.super_seeding = None
        self.tags = None
        self.time_active = None
        self.total_size = None
        self.tracker = None
        self.up_limit = None
        self.uploaded = None
        self.uploaded_session = None
        self.upspeed = None

        self.__load(data)

    def __load(self, data):
        self.added_on = data['added_on']
        self.amount_left = data['amount_left']
        self.auto_tmm = data['auto_tmm']
        self.category = data['category']
        self.completed = data['completed']
        self.completion_on = data['completion_on']
        self.dl_limit = data['dl_limit']
        self.dlspeed = data['dlspeed']
        self.downloaded = data['downloaded']
        self.downloaded_session = data['downloaded_session']
        self.eta = data['eta']
        self.f_l_piece_prio = data['f_l_piece_prio']
        self.force_start = data['force_start']
        self.hash = data['hash']
        self.last_activity = data['last_activity']
        self.magnet_uri = data['magnet_uri']
        self.max_ratio = data['max_ratio']
        self.max_seeding_time = data['max_seeding_time']
        self.name = data['name']
        self.num_complete = data['num_complete']
        self.num_incomplete = data['num_incomplete']
        self.num_leechs = data['num_leechs']
        self.num_seeds = data['num_seeds']
        self.priority = data['priority']
        self.progress = data['progress']
        self.ratio = data['ratio']
        self.ratio_limit = data['ratio_limit']
        self.save_path = data['save_path']
        self.seeding_time_limit = data['seeding_time_limit']
        self.seen_complete = data['seen_complete']
        self.seq_dl = data['seq_dl']
        self.size = data['size']
        self.state = data['state']
        self.super_seeding = data['super_seeding']
        self.tags = data['tags']
        self.time_active = data['time_active']
        self.total_size = data['total_size']
        self.tracker = data['tracker']
        self.up_limit = data['up_limit']
        self.uploaded = data['uploaded']
        self.uploaded_session = data['uploaded_session']
        self.upspeed = data['upspeed']

    def __repr__(self):
        return f"{self.name}"
