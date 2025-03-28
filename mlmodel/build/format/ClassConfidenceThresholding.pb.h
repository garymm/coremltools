// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: ClassConfidenceThresholding.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_ClassConfidenceThresholding_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_ClassConfidenceThresholding_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3019000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3019000 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/message_lite.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include "DataStructures.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_ClassConfidenceThresholding_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_ClassConfidenceThresholding_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxiliaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[1]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const uint32_t offsets[];
};
namespace CoreML {
namespace Specification {
class ClassConfidenceThresholding;
struct ClassConfidenceThresholdingDefaultTypeInternal;
extern ClassConfidenceThresholdingDefaultTypeInternal _ClassConfidenceThresholding_default_instance_;
}  // namespace Specification
}  // namespace CoreML
PROTOBUF_NAMESPACE_OPEN
template<> ::CoreML::Specification::ClassConfidenceThresholding* Arena::CreateMaybeMessage<::CoreML::Specification::ClassConfidenceThresholding>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace CoreML {
namespace Specification {

// ===================================================================

class ClassConfidenceThresholding final :
    public ::PROTOBUF_NAMESPACE_ID::MessageLite /* @@protoc_insertion_point(class_definition:CoreML.Specification.ClassConfidenceThresholding) */ {
 public:
  inline ClassConfidenceThresholding() : ClassConfidenceThresholding(nullptr) {}
  ~ClassConfidenceThresholding() override;
  explicit constexpr ClassConfidenceThresholding(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  ClassConfidenceThresholding(const ClassConfidenceThresholding& from);
  ClassConfidenceThresholding(ClassConfidenceThresholding&& from) noexcept
    : ClassConfidenceThresholding() {
    *this = ::std::move(from);
  }

  inline ClassConfidenceThresholding& operator=(const ClassConfidenceThresholding& from) {
    CopyFrom(from);
    return *this;
  }
  inline ClassConfidenceThresholding& operator=(ClassConfidenceThresholding&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ClassConfidenceThresholding& default_instance() {
    return *internal_default_instance();
  }
  static inline const ClassConfidenceThresholding* internal_default_instance() {
    return reinterpret_cast<const ClassConfidenceThresholding*>(
               &_ClassConfidenceThresholding_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(ClassConfidenceThresholding& a, ClassConfidenceThresholding& b) {
    a.Swap(&b);
  }
  inline void Swap(ClassConfidenceThresholding* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(ClassConfidenceThresholding* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  ClassConfidenceThresholding* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<ClassConfidenceThresholding>(arena);
  }
  void CheckTypeAndMergeFrom(const ::PROTOBUF_NAMESPACE_ID::MessageLite& from)  final;
  void CopyFrom(const ClassConfidenceThresholding& from);
  void MergeFrom(const ClassConfidenceThresholding& from);
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  void InternalSwap(ClassConfidenceThresholding* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "CoreML.Specification.ClassConfidenceThresholding";
  }
  protected:
  explicit ClassConfidenceThresholding(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  public:

  std::string GetTypeName() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kPrecisionRecallCurvesFieldNumber = 100,
  };
  // repeated .CoreML.Specification.PrecisionRecallCurve precisionRecallCurves = 100;
  int precisionrecallcurves_size() const;
  private:
  int _internal_precisionrecallcurves_size() const;
  public:
  void clear_precisionrecallcurves();
  ::CoreML::Specification::PrecisionRecallCurve* mutable_precisionrecallcurves(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::CoreML::Specification::PrecisionRecallCurve >*
      mutable_precisionrecallcurves();
  private:
  const ::CoreML::Specification::PrecisionRecallCurve& _internal_precisionrecallcurves(int index) const;
  ::CoreML::Specification::PrecisionRecallCurve* _internal_add_precisionrecallcurves();
  public:
  const ::CoreML::Specification::PrecisionRecallCurve& precisionrecallcurves(int index) const;
  ::CoreML::Specification::PrecisionRecallCurve* add_precisionrecallcurves();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::CoreML::Specification::PrecisionRecallCurve >&
      precisionrecallcurves() const;

  // @@protoc_insertion_point(class_scope:CoreML.Specification.ClassConfidenceThresholding)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::CoreML::Specification::PrecisionRecallCurve > precisionrecallcurves_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_ClassConfidenceThresholding_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// ClassConfidenceThresholding

// repeated .CoreML.Specification.PrecisionRecallCurve precisionRecallCurves = 100;
inline int ClassConfidenceThresholding::_internal_precisionrecallcurves_size() const {
  return precisionrecallcurves_.size();
}
inline int ClassConfidenceThresholding::precisionrecallcurves_size() const {
  return _internal_precisionrecallcurves_size();
}
inline ::CoreML::Specification::PrecisionRecallCurve* ClassConfidenceThresholding::mutable_precisionrecallcurves(int index) {
  // @@protoc_insertion_point(field_mutable:CoreML.Specification.ClassConfidenceThresholding.precisionRecallCurves)
  return precisionrecallcurves_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::CoreML::Specification::PrecisionRecallCurve >*
ClassConfidenceThresholding::mutable_precisionrecallcurves() {
  // @@protoc_insertion_point(field_mutable_list:CoreML.Specification.ClassConfidenceThresholding.precisionRecallCurves)
  return &precisionrecallcurves_;
}
inline const ::CoreML::Specification::PrecisionRecallCurve& ClassConfidenceThresholding::_internal_precisionrecallcurves(int index) const {
  return precisionrecallcurves_.Get(index);
}
inline const ::CoreML::Specification::PrecisionRecallCurve& ClassConfidenceThresholding::precisionrecallcurves(int index) const {
  // @@protoc_insertion_point(field_get:CoreML.Specification.ClassConfidenceThresholding.precisionRecallCurves)
  return _internal_precisionrecallcurves(index);
}
inline ::CoreML::Specification::PrecisionRecallCurve* ClassConfidenceThresholding::_internal_add_precisionrecallcurves() {
  return precisionrecallcurves_.Add();
}
inline ::CoreML::Specification::PrecisionRecallCurve* ClassConfidenceThresholding::add_precisionrecallcurves() {
  ::CoreML::Specification::PrecisionRecallCurve* _add = _internal_add_precisionrecallcurves();
  // @@protoc_insertion_point(field_add:CoreML.Specification.ClassConfidenceThresholding.precisionRecallCurves)
  return _add;
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::CoreML::Specification::PrecisionRecallCurve >&
ClassConfidenceThresholding::precisionrecallcurves() const {
  // @@protoc_insertion_point(field_list:CoreML.Specification.ClassConfidenceThresholding.precisionRecallCurves)
  return precisionrecallcurves_;
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace Specification
}  // namespace CoreML

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_ClassConfidenceThresholding_2eproto
