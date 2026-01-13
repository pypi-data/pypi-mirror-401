import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import re

# 自定义异常
class InvalidNoteError(ValueError):
    """自定义异常：无效的音符名"""
    pass

class InvalidScaleTypeError(ValueError):
    """自定义异常：无效的音阶类型"""
    pass

class InvalidChordTypeError(ValueError):
    """自定义异常：无效的和弦类型"""
    pass

class InvalidNoteDurationError(ValueError):
    """自定义异常：无效的音符时长参数"""
    pass

class InvalidBPMError(ValueError):
    """自定义异常：无效的速度（BPM）参数"""
    pass

class InvalidDirectionError(ValueError):
    """自定义异常：无效的音阶方向参数"""
    pass

# 核心常量定义（专业音乐记法：中央C=C1，标准音A1=440Hz）
# 12个半音的物理音名（用于索引计算，统一用英文#）
PHYSICAL_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
# 基础音名（无升降）
BASE_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
# 带升降的完整音名映射（关键：统一字符编码）
NOTE_ENHARMONIC_MAP = {
    # 降音（♭）：大调修正专用
    'A♭': 'G#', 
    'B♭': 'A#',
    # 升音（♯）：小调修正专用（关键：♯映射到#）
    'F♯': 'F#', 
    'G♯': 'G#',
    # 基础音名
    'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'A': 'A', 'B': 'B'
}

# 自然音阶的半音间隔（大调和小调）
NATURAL_SCALE_SEMITONES = {
    'maj': [0, 2, 4, 5, 7, 9, 11],  # 自然大调：I,II,III,IV,V,VI,VII级
    'min': [0, 2, 3, 5, 7, 8, 10]   # 自然小调：I,II,III,IV,V,VI,VII级
}

# 音阶修正规则（核心：完善下行修正逻辑）
SCALE_MODIFICATIONS = {
    # 和声音阶修正（上下行一致）
    'maj_har': {
        'up': [(5, 'flat')],  # 大调和声上行：VI级降半音（A→A♭）
        'down': [(5, 'flat')] # 大调和声下行：VI级降半音（A→A♭）
    },
    'min_har': {
        'up': [(6, 'sharp')],  # 小调和声上行：VII级升半音（G→G♯）
        'down': [(6, 'sharp')] # 小调和声下行：VII级升半音（G→G♯）
    },
    # 旋律音阶修正（上行修正，下行还原为自然音阶）
    'maj_mel': {
        'up': [(5, 'flat'), (6, 'flat')],  # 旋律大调上行：VI级A♭，VII级B♭
        'down': []  # 旋律大调下行：还原为自然大调（无降号）
    },
    'min_mel': {
        'up': [(5, 'sharp'), (6, 'sharp')],  # 旋律小调上行：VI级F♯，VII级G♯
        'down': []  # 旋律小调下行：还原为自然小调（无升号）
    },
    # 自然音阶无修正
    'maj_nat': {'up': [], 'down': []},
    'min_nat': {'up': [], 'down': []}
}

# 支持的参数列表
SCALE_VARIANTS = ['nat', 'har', 'mel']
SCALE_DIRECTIONS = ['up', 'down']
SCALE_MODES = ['maj', 'min']
SUPPORTED_DURATIONS = [4, 2, 1, 0.5, 0.25, 0.125]
CHORD_STRUCTURES = {
    'triad': [0, 2, 4],        # 三和弦（I, III, V级）
    'seventh': [0, 2, 4, 6]    # 七和弦（I, III, V, VII级）
}

# 音频基础参数
SAMPLE_RATE = 44100
VOLUME = 0.2
DEFAULT_BPM = 120
DEFAULT_NOTE_DURATION = 1
SCALE_NOTE_GAP = 0.1

# 标准音定义
STANDARD_NOTE = 'A1'
STANDARD_FREQ = 440.0
STANDARD_PHYSICAL_INDEX = PHYSICAL_NOTES.index('A')

def _parse_note_with_mode(note_str: str) -> tuple:
    """解析带调式的根音字符串"""
    if '_' in note_str:
        note_part, mode = note_str.split('_')
        mode = mode.lower()
        if mode not in SCALE_MODES:
            raise InvalidNoteError(f"无效的调式：{mode}，支持 {SCALE_MODES}")
    else:
        note_part = note_str
        mode = 'maj'

    pattern = r'^([A-G])(\d+)$'
    match = re.match(pattern, note_part.strip(), re.IGNORECASE)
    if not match:
        raise InvalidNoteError(
            f"无效的根音格式：{note_part}，正确格式示例：C1、A1、D2"
        )
    note_name = match.group(1).upper()
    octave = int(match.group(2))
    if note_name not in BASE_NOTES:
        raise InvalidNoteError(
            f"无效的音名：{note_name}，合法音名：{', '.join(BASE_NOTES)}"
        )
    return note_name, octave, mode

def _calculate_note_duration_ms(duration: float, bpm: int) -> int:
    """计算音符时长（毫秒）"""
    if duration not in SUPPORTED_DURATIONS:
        raise InvalidNoteDurationError(
            f"无效的音符时长：{duration}，支持的时长：{SUPPORTED_DURATIONS}"
        )
    if not isinstance(bpm, int) or bpm <= 0 or bpm > 300:
        raise InvalidBPMError(
            f"无效的速度（BPM）：{bpm}，请输入 1-300 之间的整数"
        )
    quarter_note_sec = 60 / bpm
    note_duration_sec = quarter_note_sec * duration
    return int(note_duration_sec * 1000)

def _modify_degree(note_name: str, modification_type: str) -> str:
    """修正音级，返回带升降号的理论记谱名"""
    if modification_type == 'flat':
        # 大调降半音
        flat_map = {'A': 'A♭', 'B': 'B♭'}
        if note_name in flat_map:
            return flat_map[note_name]
        else:
            raise InvalidNoteError(f"大调不支持对 {note_name} 进行降半音修正")
    elif modification_type == 'sharp':
        # 小调升半音
        sharp_map = {'F': 'F♯', 'G': 'G♯'}
        if note_name in sharp_map:
            return sharp_map[note_name]
        else:
            raise InvalidNoteError(f"小调不支持对 {note_name} 进行升半音修正")
    else:
        return note_name

def _get_physical_note(theoretical_note: str) -> str:
    """将理论记谱名转换为物理音名（兼容♯和#）"""
    theoretical_note = theoretical_note.replace('#', '♯')
    return NOTE_ENHARMONIC_MAP.get(theoretical_note, theoretical_note)

def calculate_frequency(theoretical_note_str: str) -> float:
    """计算音符频率（支持 A♭1、F♯2 等格式）"""
    # 拆分音名和八度
    if '♭' in theoretical_note_str:
        note_name = theoretical_note_str[:2]
        octave_str = theoretical_note_str[2:]
    elif '♯' in theoretical_note_str or '#' in theoretical_note_str:
        note_name = theoretical_note_str[:2].replace('#', '♯')
        octave_str = theoretical_note_str[2:]
    else:
        note_name = theoretical_note_str[:1]
        octave_str = theoretical_note_str[1:]
    
    if not octave_str.isdigit():
        raise InvalidNoteError(f"无效的音符格式：{theoretical_note_str}，八度必须是数字")
    
    octave = int(octave_str)
    physical_note = _get_physical_note(note_name)
    
    if physical_note not in PHYSICAL_NOTES:
        raise InvalidNoteError(f"无效的物理音名：{physical_note}（理论记谱名：{note_name}）")
    
    physical_index = PHYSICAL_NOTES.index(physical_note)
    semitone_diff = (octave - 1) * 12 + (physical_index - STANDARD_PHYSICAL_INDEX)
    frequency = STANDARD_FREQ * (2 ** (semitone_diff / 12))
    return round(frequency, 2)

def note(theoretical_note_str: str) -> dict:
    """生成音符详细信息"""
    frequency = calculate_frequency(theoretical_note_str)
    # 拆分音名和八度
    if '♭' in theoretical_note_str:
        theo_name = theoretical_note_str[:2]
        octave = int(theoretical_note_str[2:])
    elif '♯' in theoretical_note_str or '#' in theoretical_note_str:
        theo_name = theoretical_note_str[:2].replace('#', '♯')
        octave = int(theoretical_note_str[2:])
    else:
        theo_name = theoretical_note_str[:1]
        octave = int(theoretical_note_str[1:])
    
    return {
        'full_name': theoretical_note_str,
        'theoretical_name': theo_name,
        'octave': octave,
        'physical_note': _get_physical_note(theo_name),
        'frequency': frequency
    }

def _generate_natural_scale(root_note_str: str, mode: str) -> list:
    """生成自然音阶（上行：I→VII 级）"""
    root_name, root_octave, _ = _parse_note_with_mode(root_note_str)
    root_physical_index = PHYSICAL_NOTES.index(root_name)
    scale_semitones = NATURAL_SCALE_SEMITONES[mode]
    natural_scale = []
    
    for semitone in scale_semitones:
        current_physical_index = (root_physical_index + semitone) % 12
        octave_offset = (root_physical_index + semitone) // 12
        current_octave = root_octave + octave_offset
        physical_note = PHYSICAL_NOTES[current_physical_index]
        base_note = physical_note.replace('#', '')
        natural_scale.append(f"{base_note}{current_octave}")
    
    return natural_scale

def scale(root_note_str: str, property: str, start: str = None, direction: str = 'up') -> dict:
    """
    生成指定音阶（下行时从 VII 级到 I 级，符合音乐理论）
    Args:
        root_note_str: 根音（如 C1_maj、A1_min）
        property: 音阶类型（nat/har/mel）
        start: 起始音（仅上行有效，下行固定从 VII 级开始）
        direction: 方向（up/down）
    Returns:
        dict: 音阶详细信息
    """
    # 参数校验
    if property not in SCALE_VARIANTS:
        raise InvalidScaleTypeError(f"无效的音阶类型：{property}，支持：{SCALE_VARIANTS}")
    if direction not in SCALE_DIRECTIONS:
        raise InvalidDirectionError(f"无效的音阶方向：{direction}，支持：{SCALE_DIRECTIONS}")
    root_name, root_octave, root_mode = _parse_note_with_mode(root_note_str)

    # 1. 生成自然音阶（上行：I→VII 级）
    natural_scale_up = _generate_natural_scale(root_note_str, root_mode)
    # 2. 生成下行自然音阶（VII→I 级，反转上行音阶）
    natural_scale_down = natural_scale_up[::-1]

    # 3. 获取修正规则
    scale_key = f"{root_mode}_{property}"
    modifications = SCALE_MODIFICATIONS[scale_key][direction]

    # 4. 生成基础音阶（根据方向选择上行或下行自然音阶）
    if direction == 'up':
        base_scale = natural_scale_up.copy()
    else:
        base_scale = natural_scale_down.copy()

    # 5. 修正音阶（应用调式修正规则）
    modified_scale = base_scale.copy()
    for (degree_index, mod_type) in modifications:
        # 下行时：修正的是反转后音阶的对应音级（基于原上行音阶的索引）
        if direction == 'down':
            # 原上行音阶的索引 → 下行音阶的索引（反转后）
            original_up_index = 6 - degree_index  # VII级（6）→ 0，VI级（5）→ 1，依此类推
            current_note_index = original_up_index
        else:
            current_note_index = degree_index
        
        # 拆分音符并修正
        original_note = modified_scale[current_note_index]
        if len(original_note) >= 2 and original_note[1].isdigit():
            original_note_name = original_note[:1]
            original_octave = original_note[1:]
        else:
            original_note_name = original_note[:-1]
            original_octave = original_note[-1]
        
        new_note_name = _modify_degree(original_note_name, mod_type)
        modified_scale[current_note_index] = f"{new_note_name}{original_octave}"

    # 6. 处理起始音（仅上行有效，下行固定从 VII 级开始）
    if direction == 'up' and start is not None:
        if start not in natural_scale_up:
            raise InvalidNoteError(f"起始音 {start} 不在自然音阶中：{natural_scale_up}")
        start_index = natural_scale_up.index(start)
        modified_scale = modified_scale[start_index:] + modified_scale[:start_index]

    # 7. 计算频率
    scale_freqs = [calculate_frequency(note) for note in modified_scale]

    # 8. 生成音阶名称
    scale_mode_cn = {'maj': '大调', 'min': '小调'}
    scale_variant_cn = {'nat': '自然', 'har': '和声', 'mel': '旋律'}
    direction_cn = {'up': '上行（I→VII）', 'down': '下行（VII→I）'}
    scale_type_cn = f"{scale_variant_cn[property]}{scale_mode_cn[root_mode]}（{direction_cn[direction]}）"

    return {
        'root': f"{root_name}{root_octave}_{root_mode}",
        'type': scale_type_cn,
        'property': property,
        'direction': direction,
        'start_note': modified_scale[0],  # 下行时起始音为 VII 级
        'end_note': modified_scale[-1],   # 下行时结束音为 I 级
        'notes': modified_scale,
        'frequencies': scale_freqs,
        'natural_scale_up': natural_scale_up,    # 上行自然音阶（I→VII）
        'natural_scale_down': natural_scale_down, # 下行自然音阶（VII→I）
        'modifications': modifications
    }

def chord(root_note_str: str, property: str, chord_type: str = 'triad', direction: str = 'up') -> dict:
    """生成和弦"""
    if chord_type not in CHORD_STRUCTURES:
        raise InvalidChordTypeError(f"无效的和弦类型：{chord_type}，支持：{CHORD_STRUCTURES.keys()}")
    root_scale = scale(root_note_str, property, start=None, direction=direction)
    chord_indices = CHORD_STRUCTURES[chord_type]
    chord_notes = [root_scale['notes'][i] for i in chord_indices]
    chord_freqs = [root_scale['frequencies'][i] for i in chord_indices]
    return {
        'root': root_note_str,
        'scale_type': root_scale['type'],
        'chord_type': '三和弦' if chord_type == 'triad' else '七和弦',
        'notes': chord_notes,
        'frequencies': chord_freqs
    }

def _generate_audio_wave(frequency: float, duration_ms: int) -> AudioSegment:
    """生成音频波形"""
    duration_sec = duration_ms / 1000
    num_samples = int(SAMPLE_RATE * duration_sec)
    t = np.linspace(0, duration_sec, num_samples, endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t)
    wave = (wave * VOLUME * 32767).astype(np.int16)
    return AudioSegment(
        wave.tobytes(),
        frame_rate=SAMPLE_RATE,
        sample_width=2,
        channels=1
    )

def _generate_chord_audio(chord_freqs: list, duration_ms: int) -> AudioSegment:
    """生成和弦音频"""
    chord_audio = AudioSegment.silent(duration=duration_ms)
    for freq in chord_freqs:
        note_audio = _generate_audio_wave(freq, duration_ms)
        chord_audio = chord_audio.overlay(note_audio)
    return chord_audio

class Musi:
    """音乐工具类（支持下行音阶从 VII 到 I 级）"""
    def calculate_frequency(self, theoretical_note_str: str) -> float:
        return calculate_frequency(theoretical_note_str)
    
    def note(self, theoretical_note_str: str) -> dict:
        return note(theoretical_note_str)
    
    def scale(self, root_note_str: str, property: str, start: str = None, direction: str = 'up') -> dict:
        return scale(root_note_str, property, start, direction)
    
    def chord(self, root_note_str: str, property: str, chord_type: str = 'triad', direction: str = 'up') -> dict:
        return chord(root_note_str, property, chord_type, direction)
    
    def play_note(self, theoretical_note_str: str, duration: float = DEFAULT_NOTE_DURATION, bpm: int = DEFAULT_BPM):
        """播放单个音符"""
        note_duration_ms = _calculate_note_duration_ms(duration, bpm)
        note_info = self.note(theoretical_note_str)
        print(f"播放音符：{note_info['full_name']}（物理音名：{note_info['physical_note']} | 频率：{note_info['frequency']}Hz）")
        print(f"时长：{duration}分音符 | 速度：{bpm} BPM | 实际时长：{note_duration_ms}ms")
        audio = _generate_audio_wave(note_info['frequency'], note_duration_ms)
        play(audio)
    
    def play_scale(self, root_note_str: str, property: str, start: str = None, direction: str = 'up',
                   duration: float = DEFAULT_NOTE_DURATION, bpm: int = DEFAULT_BPM):
        """播放音阶（下行时从 VII 级到 I 级）"""
        note_duration_ms = _calculate_note_duration_ms(duration, bpm)
        gap_ms = int(SCALE_NOTE_GAP * (60 / bpm) * 1000)
        scale_info = self.scale(root_note_str, property, start, direction)
        print(f"播放：{scale_info['type']} 音阶")
        print(f"音阶：{scale_info['notes']}")
        print(f"时长：{duration}分音符 | 速度：{bpm} BPM | 单个音符时长：{note_duration_ms}ms")
        scale_audio = AudioSegment.silent(duration=0)
        for freq in scale_info['frequencies']:
            note_audio = _generate_audio_wave(freq, note_duration_ms)
            scale_audio += note_audio
            scale_audio += AudioSegment.silent(duration=gap_ms)
        play(scale_audio)
    
    def play_chord(self, root_note_str: str, property: str, chord_type: str = 'triad', direction: str = 'up',
                   duration: float = DEFAULT_NOTE_DURATION, bpm: int = DEFAULT_BPM):
        """播放和弦"""
        note_duration_ms = _calculate_note_duration_ms(duration, bpm)
        chord_info = self.chord(root_note_str, property, chord_type, direction)
        print(f"播放：{chord_info['scale_type']} {chord_info['chord_type']}")
        print(f"组成音符：{chord_info['notes']}")
        print(f"时长：{duration}分音符 | 速度：{bpm} BPM | 实际时长：{note_duration_ms}ms")
        audio = _generate_chord_audio(chord_info['frequencies'], note_duration_ms)
        play(audio)
    
    def export_scale(self, root_note_str: str, property: str, output_path: str, start: str = None, direction: str = 'up',
                     duration: float = DEFAULT_NOTE_DURATION, bpm: int = DEFAULT_BPM):
        """导出音阶为WAV"""
        note_duration_ms = _calculate_note_duration_ms(duration, bpm)
        gap_ms = int(SCALE_NOTE_GAP * (60 / bpm) * 1000)
        scale_info = self.scale(root_note_str, property, start, direction)
        scale_audio = AudioSegment.silent(duration=0)
        for freq in scale_info['frequencies']:
            note_audio = _generate_audio_wave(freq, note_duration_ms)
            scale_audio += note_audio
            scale_audio += AudioSegment.silent(duration=gap_ms)
        scale_audio.export(output_path, format="wav")
        print(f"{scale_info['type']} 音阶已导出至：{output_path}")
        print(f"音阶：{scale_info['notes']}")
    
    def export_chord(self, root_note_str: str, property: str, output_path: str, chord_type: str = 'triad', direction: str = 'up',
                     duration: float = DEFAULT_NOTE_DURATION, bpm: int = DEFAULT_BPM):
        """导出和弦为WAV"""
        note_duration_ms = _calculate_note_duration_ms(duration, bpm)
        chord_info = self.chord(root_note_str, property, chord_type, direction)
        audio = _generate_chord_audio(chord_info['frequencies'], note_duration_ms)
        audio.export(output_path, format="wav")
        print(f"{chord_info['scale_type']} {chord_info['chord_type']} 已导出至：{output_path}")

# 实例化
musi = Musi()

